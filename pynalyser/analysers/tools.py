from typing import Any, Dict, List

import attr

from .. import acr
from .. import portable_ast as ast


@attr.s(auto_attribs=True)
class AnalysisContext:
    modules: List[acr.Module]
    results: Dict[str, Any] = attr.ib(init=False, factory=lambda: dict())


class Analyser(acr.NodeVisitor):
    context: AnalysisContext

    def analyse(self, ctx: AnalysisContext) -> None:
        self.context = ctx
        self.start(ctx.modules[0])


class NameCollector(acr.NodeVisitor):
    # accounted for:
    # Attribute - don't visit fields, XXX: for now
    # Subscript - don't visit fields
    # Starred - just visit itself
    # Name - add name, if we got here
    # List - just visit itself
    # Tuple - just visit itself
    # other nodes AFAIK will not appear here

    _collected_names: List[str] = []

    def collect_names(self, node: ast.AST) -> List[str]:
        self._collected_names.clear()
        self.visit(node)
        return self._collected_names

    def visit_Attribute(self, node: ast.Attribute) -> None:
        pass

    def visit_Subscript(self, node: ast.Subscript) -> None:
        pass

    def visit_Name(self, node: ast.Name) -> None:
        self._collected_names.append(node.id)
