from model import NeuralNet
from mesa.mesa_logging import DEBUG, log_to_stderr
from smell import Food 
from mesa.visualization import (
    SolaraViz,
    make_plot_component,
    make_space_component,
)

log_to_stderr(DEBUG)


def agent_portrayal(agent):
    portrayal = {
        "size": 800,
        "color": "tab:orange" if isinstance(agent,Food) else "tab:blue"
    }

    return portrayal

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
}

def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().set_size_inches(10, 10)

# Create initial model instance
model = NeuralNet(1, 5)

SpaceGraph = make_space_component(
    agent_portrayal, post_process=post_process
)
CreaturePlot = make_plot_component({"Fullness":"#FE6100", "SmellUp":"#FF0000", "SmellDown":"#3CB371"})
Neuron1Plot = make_plot_component({"fullWeight1":"#FFDAB9", "SmellWeight1":"#3CB371"})
Neuron2Plot = make_plot_component({"fullWeight2":"#FFDAB9", "SmellWeight2":"#3CB371"})
PotentialPlot = make_plot_component({"forward PT":"#FE6100", "backward PT":"#FF0000"})
page = SolaraViz(
    model,
    components=[SpaceGraph, CreaturePlot, Neuron1Plot, Neuron2Plot,PotentialPlot],
    model_params=model_params,
    name="Neural Network",
)
page  # noqa


