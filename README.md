#  Drone Swarm Project

The **Drone Swarm Project** is a simulation and coordination platform designed to study, visualize, and optimize swarm intelligence in autonomous drones.  
It enables real-time simulation of cooperative strategies for drone fleets, including defense, asset protection, and adversarial engagements.  
The project combines **FastAPI** (backend for swarm logic and APIs) and **React.js** (frontend for interactive visualization) in a modular architecture.  

---

## 🛠 Tech Stack

### Backend
- FastAPI
- Python (Asyncio, WebSockets)
- Simulation & Swarm Coordination Algorithms

### Frontend
- React.js (with Vite)
- Tailwind CSS
- Recharts (data visualization)
- Framer Motion (animations)

---

##  Features
- Real-time drone swarm simulation and visualization  
- Configurable swarm parameters (speed, range, coordination strategy)  
- Enemy drone detection and engagement logic  
- Dashboard with charts and logs for swarm activity  
- WebSocket-based live updates between backend and frontend  
- Modular architecture for extending swarm strategies  

---

##  Project Structure
/
├── backend/
│ ├── api/ # FastAPI route handlers
│ ├── simulation/ # Core swarm coordination & logic
│ ├── models/ # Data structures (Pydantic)
│ ├── services/ # Simulation manager, WebSocket services
│ ├── utils/ # Helper functions
│ ├── main.py # FastAPI entrypoint
│ └── requirements.txt # Backend dependencies
│
├── frontend/
│ ├── src/
│ │ ├── components/ # React components (Drone, SimulationScreen, Dashboard, etc.)
│ │ ├── pages/ # Views/screens
│ │ ├── assets/ # Images, icons, etc.
│ │ └── App.jsx # Main app entry
│ ├── public/ # Static files
│ ├── tailwind.config.js # Tailwind setup
│ └── package.json # Frontend dependencies
│
└── README.md # Project documentation


### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```



### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```



## API Documentation

After starting the backend, visit:

 http://localhost:8000/docs

This provides a full list of API endpoints and testable documentation via Swagger UI.



## Development Workflow

Backend initializes swarm simulation and exposes APIs.

Frontend dashboard connects via WebSocket to stream drone state updates.

Drones are visualized on a 2D simulation screen.

Enemy drones and assets appear, triggering coordination logic.

Simulation events are logged and displayed in real-time charts.

Developers can tweak parameters and re-run simulations instantly.