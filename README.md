# **Energy Marketplace for Sri Lanka Microgrid**

This repository implements an Energy Marketplace System designed for a microgrid setup in Sri Lanka. The system enables intelligent energy management and pricing strategies among distributed energy resources like solar PV, battery storage, and diesel generators within an isolated microgrid. The solution includes agent-based control, a dynamic pricing algorithm, and a simple FastAPI for integration and monitoring.

## 🔧 Project Structure**

<pre> EnergyMarketplaceForSriLankaMicrogrid/ 
├── API_Route/ # RESTful API endpoint functions 
├── EMS/ # Energy Management System (EMS) core logic and agent classes 
├── PriceAlgorithm/ # Dynamic electricity pricing algorithm 
├── init.py # Entry-point script to initialize the system 
├── requirement.txt # List of required Python packages 
└── README.md # Project overview and setup instructions </pre>

## ⚙️ Features

- Agent-based architecture for EMS design to match the demand and supply priorotizing the Solar, and battery.
- Dynamic pricing based on hourly demand-supply balance.  
- FastAPI for external data access and integration.

## 🚀 Getting Started
### Prerequisites
Ensure you have Python 3.8+ installed.

Install required packages:
<pre> pip install -r requirement.txt </pre>
### Running the System

<pre> python init.py</pre>
This will start the EMS system with all relevant agents and pricing logic.

## 📁 Modules
- EMS/: Contains the EMS agent definitions and logic for handling energy flow.
- PriceAlgorithm/: Contains logic to compute hourly energy prices dynamically.
- API_Route/: API functions to expose EMS data and hourly tarrif for next 24 hours.

## 🧠 Purpose

The primary goal of this system is to **increase the utilization of renewable energy sources**, particularly **solar energy**, by implementing **reduced tariffs during daytime hours**. This encourages consumers to shift their usage to periods of high solar availability, promoting optimal use of locally generated clean energy. 

Ultimately, the system aims to pave the way for a **sustainable energy future** by enabling smarter consumption patterns, lowering reliance on fossil fuels, and enhancing microgrid efficiency through intelligent agent-based energy management and dynamic pricing strategies.
