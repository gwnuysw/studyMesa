from model import NeuralNet
from mesa.mesa_logging import DEBUG, log_to_stderr
from mesa.visualization import (
    SolaraViz,
    make_plot_component,
    make_space_component,
)

log_to_stderr(DEBUG)


def agent_portrayal(agent):
    portrayal = {
        "size": 800,
    }

    return portrayal

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": 10,
    "height": 10,
}

def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().set_size_inches(10, 10)

# Create initial model instance
model = NeuralNet(10, 10)

SpaceGraph = make_space_component(
    agent_portrayal, post_process=post_process
)
CreaturePlot = make_plot_component({"Fullness":"#FE6100", "Predator":"#FF0000"})

page = SolaraViz(
    model,
    components=[SpaceGraph, CreaturePlot],
    model_params=model_params,
    name="Neural Network",
)
page  # noqa


