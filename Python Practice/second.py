
from first import Brand


class Car(Brand):
    def __init__(self, name , model):
        super().__init__(name, model)
        
    
details = Brand("honda", 1999)
print(details)

            
        