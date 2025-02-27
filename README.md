# TUEvolution

## Description
TUEvolution is a simulation project for the Scientific Computing for Mechanical Engineering course. It simulates the behavior and evolution of creatures in a virtual world. The simulation is inspired by the YouTuber ["Primer"](https://www.youtube.com/channel/UCKzJFdi57J53Vr_BkTfN3uQ), who creates educational content on evolutionary biology and complex systems.

## Background
The simulation models a population of creatures that interact with their environment and each other. Creatures can move, reproduce, and perish based on various factors such as food availability and environmental conditions. The goal is to observe how different traits and behaviors evolve over time in response to the simulated environment.

## Assignment instructions
The assignment instructions can be found [here](https://tue-4em30.github.io/SC4ME_OOP/20).

## Installation
To install the required dependencies, run:
```sh
pip install -r requirements.txt
```

## Usage
To run the simulation, execute the following command:
```sh
python TUEvolution/main.py
```

## Project structure
```
TUEvolution/
│
├── README.md
├── setup.py
├── requirements.txt
├── TUEvolution/
│   ├── __init__.py
│   ├── main.py
│   ├── map.py
│   ├── creatures.py
│   ├── graphs.py
│   └── ...
│
├── scenarios/
│   ├── default.toml
│   ├── question1.toml
│   └── ...
|
├── tests/
│   ├── __init__.py
│   ├── test_creatures.py
│   └── ...
│
└── ...
```