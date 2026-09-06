from dataclasses import dataclass

@dataclass #this creates constructor for us kinnda like lombok in springboot
class RequestContext:
    user_id : str
    tenant_id : str #this tells us which organisation the user is in
    role : str