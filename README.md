# junction-x-budapest

Winner solution for JunctionX Budapest hackathon, Varian challenge, Radiotherapy Treatment Optimization problem. 

Application which helps doctors with optimization of Radiation Therapy Treatments - even distribution of the linear accelerator's load. Every week, radiotherapy centers face the complex task of scheduling hundreds of treatment sessions amongst the available linear accelerators. With the increase in cancer patient numbers, manually creating a feasible and efficient schedule has shown to be a difficult, time-consuming task. It is utter of importance to have maximized utilization of linear accelerators or with other words a linear accelerator in stand-by is a missed opportunity to treat a patient.


To launch web-backend and streamlit demo app use docker-compose: `docker-compose up -d`. Applications will be available on 8501 and 8000 ports.

To visualise an algorithm:
- create virtual environment `virtualenv venv`
- activate virtual environment `source venv/bin/activate`
- `cd predictor/app`
- install python requirements `pip install -r requirements.txt`
- run app `python main.py`
 
