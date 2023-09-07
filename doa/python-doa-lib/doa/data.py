"module for dataclasses commonly used."
from dataclasses import dataclass, field


@dataclass
class FKRelationResult:
    "FK relation dataclass."
    columns: list[str]
    referenced_table: str
    referenced_columns: list[str]


@dataclass
class TableAnalysisResult:
    "Table analysis result of FK analysis results."
    table_name: str
    columns: list[str] = field(init=False, default_factory=list)
    # pylint: disable=invalid-name
    FKs: list[FKRelationResult] = field(init=False, default_factory=list)

    def add_column(self, name: str):
        "add a data of a column."
        self.columns.append(name)

    def add_FK(self, col_names, ref_table, ref_col_names):  # pylint: disable=invalid-name
        "add a data of a FK relation."
        self.FKs.append(FKRelationResult(columns=col_names, referenced_table=ref_table,
                                         referenced_columns=ref_col_names))

    # def exit(self) -> dict[str, Any]:
    #     return {"name": self.table_name, "columns": self.columns}
