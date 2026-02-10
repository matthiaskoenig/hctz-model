from pathlib import Path

from pkdb_models.models.data import collect_tsv_files

def collect_hctz_data():
    common_parent: Path = Path(__file__).parents[5]
    source_dir = common_parent / "pkdb_data" / "studies" / "hydrochlorothiazide"
    target_dir = Path(__file__).parent / "hydrochlorothiazide"

    collect_tsv_files(source_dir=source_dir, target_dir=target_dir)


    def is_Devineni2014(study_name) -> bool:
        return study_name == "Devineni2014"

    collect_tsv_files(
        source_dir=common_parent / "pkdb_data" / "studies" / "canagliflozin",
        target_dir=Path(__file__).parent / "canagliflozin",
        filter_study=is_Devineni2014,
    )

    def is_Koytchev2004(study_name) -> bool:
        return study_name == "Koytchev2004"

    collect_tsv_files(
        source_dir=common_parent / "pkdb_data" / "studies" / "lisinopril",
        target_dir=Path(__file__).parent / "lisinopril",
        filter_study=is_Koytchev2004,
    )

    def is_Niopas2011(study_name) -> bool:
        return study_name == "Niopas2011"

    collect_tsv_files(
        source_dir=common_parent / "pkdb_data" / "studies" / "enalapril",
        target_dir=Path(__file__).parent / "enalapril",
        filter_study=is_Niopas2011,
    )

    def is_Vaidyanathan2006(study_name) -> bool:
        return study_name == "Vaidyanathan2006"

    collect_tsv_files(
        source_dir=common_parent / "pkdb_data" / "studies" / "aliskiren",
        target_dir=Path(__file__).parent / "aliskiren",
        filter_study=is_Vaidyanathan2006,
    )


if __name__ == "__main__":
    collect_hctz_data()

