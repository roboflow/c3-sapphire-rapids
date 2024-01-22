from roboflow import Roboflow

API_KEY = "api_key"
WORKSPACE = "workspace_name"
PROJECT = "project_name"
rf = Roboflow(api_key= API_KEY)

project = rf.workspace(WORKSPACE).project(PROJECT)
settings = {
 "augmentation": {
    "bbblur": { "pixels": 1.5 },
    "bbbrightness": { "brighten": True, "darken": False, "percent": 91 }
    },
 "preprocessing": {
    "contrast": { "type": "Contrast Stretching" },
    "filter-null": { "percent": 50 },
    "grayscale": True,
    }
 
 }
                        
versions = project.generate_version(settings=settings)