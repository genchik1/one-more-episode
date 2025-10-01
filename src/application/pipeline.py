from typing import Self

from src.application.errors import PipelineError
from src.application.stages.errors import StageError
from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineBuilder, IPipelineStage


class Pipeline(IPipelineBuilder):
    def __init__(self, stages: list[IPipelineStage] = None) -> None:
        self.stages = stages or []

    def add_stage(self, stage: IPipelineStage) -> Self:
        self.stages.append(stage)
        return self

    async def execute(self) -> ItemsCollection:
        data = ItemsCollection()
        for stage in self.stages:
            try:
                data = await stage.process(data)
            except StageError as e:
                raise PipelineError(f"Stage {stage.__class__} failed") from e
        return data

    def __rshift__(self, other: IPipelineStage) -> Self:
        return self.add_stage(other)
