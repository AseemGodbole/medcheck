from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

try:
    from acb_calculator import lookup_drug
except ModuleNotFoundError:  # pragma: no cover - fallback for package-style imports
    from calculators.acb_calculator import lookup_drug


_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")
_STRENGTH_RE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|iu|units?|%)\b")
_DOSE_LIST_RE = re.compile(r"\b\d+(?:/\d+)+(?:\s*(?:mg|mcg|g|ml|iu|units?|%))?\b")
_FORM_RE = re.compile(
    r"\b(?:tablet|tablets|tab|capsule|capsules|cap|syrup|suspension|solution|injection|inhaler|spray|drop|drops|cream|ointment|gel|patch|powder|granules?|lozenge|sachet|pellet|film|oral|wash|lotion|suppository|gel|puff|metered|mr|sr|cr|er|od|bd|tds)\b"
)


def _normalize(value: str) -> str:
    return _NORMALIZE_RE.sub(" ", value.lower()).strip()


def _strip_strength_and_form(value: str) -> str:
    cleaned = value.lower().replace("-", " ").replace("/", " ")
    cleaned = _STRENGTH_RE.sub(" ", cleaned)
    cleaned = _DOSE_LIST_RE.sub(" ", cleaned)
    cleaned = re.sub(r"\b\d+\b", " ", cleaned)
    cleaned = _FORM_RE.sub(" ", cleaned)
    cleaned = _NORMALIZE_RE.sub(" ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _extract_generics(prefix_blob: str, composition_blob: str) -> list[str]:
    if not prefix_blob and not composition_blob:
        return []

    generics: list[str] = []

    # The first ingredient often gets glued to the company name in the raw CSV row.
    prefix_words = re.findall(r"[A-Z][a-z]+", prefix_blob)
    if prefix_words:
        first_generic = _normalize(prefix_words[-1])
        if first_generic and first_generic not in {"ltd", "pvt", "pharma", "labs", "biotech", "healthcare", "remedies"}:
            generics.append(first_generic)

    text = composition_blob.replace("ADD", " ").replace("not available", " ")
    for match in re.findall(r"([A-Z][A-Za-z0-9/-]*(?:\s+[A-Z][A-Za-z0-9/-]*)*)\s*\(", text):
        chunk = _normalize(match)
        if not chunk or chunk in {"na", "n a", "not available"}:
            continue
        generics.append(chunk)

    return generics


@lru_cache(maxsize=1)
def _load_brand_map() -> dict[str, list[str]]:
    dataset_path = Path(__file__).resolve().parent.parent / "India Medicines and Drug Info Dataset.csv"
    brand_map: dict[str, list[str]] = {}

    if not dataset_path.exists():
        return brand_map

    with dataset_path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        next(handle, None)
        for raw_line in handle:
            split_point = raw_line.find('",')
            if split_point == -1:
                continue

            payload = raw_line[split_point + 2 :].rstrip("\n")
            parts = payload.split(",")
            if len(parts) < 5:
                continue

            brand_name = parts[0].strip()
            prefix_blob = parts[3].strip() if len(parts) > 3 else ""
            composition_blob = ",".join(parts[4:]).strip() if len(parts) > 4 else parts[-1].strip()

            if not brand_name or not (prefix_blob or composition_blob):
                continue

            generics = _extract_generics(prefix_blob, composition_blob)
            if not generics:
                continue

            aliases = {
                _normalize(brand_name),
                _strip_strength_and_form(brand_name),
            }
            aliases.discard("")

            for alias in aliases:
                mapped = brand_map.setdefault(alias, [])
                for generic in generics:
                    if generic not in mapped:
                        mapped.append(generic)

    return brand_map


def resolve_drug_name(name: str) -> tuple[list[str], str]:
    """Resolve a user-entered drug name into one or more canonical generic names."""
    raw = (name or "").strip()
    if not raw:
        return [], "empty"

    direct = lookup_drug(raw)
    if direct:
        canonical, *_ = direct
        return [canonical], "curated"

    normalized = _normalize(raw)
    stripped = _strip_strength_and_form(raw)
    brand_map = _load_brand_map()

    for candidate in (stripped, normalized):
        if candidate and candidate in brand_map:
            return brand_map[candidate], "dataset"

    return [raw], "unchanged"


def resolve_drug_names(drug_names: list[str]) -> tuple[list[str], list[str]]:
    """Expand brand names to generic names while preserving original names when unresolved."""
    expanded: list[str] = []
    notes: list[str] = []

    for drug in drug_names:
        resolved, source = resolve_drug_name(drug)
        expanded.extend(resolved)

        if source in {"curated", "dataset"} and resolved and resolved != [drug.strip()]:
            notes.append(f"{drug.strip()} -> {', '.join(resolved)}")

    return expanded, notes