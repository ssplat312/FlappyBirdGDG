from entity import ObjectEntety
import pygame

#Manages every entity and checks if certain entities collide with each other
class EntityManager():

    def __init__(self):
        self.entityList:list[ObjectEntety] = []
        
        
    #Updates the delta time using the static variable
    def UpdateDeltaTime(self, newDT):
        ObjectEntety.dt = newDT
        
    #Updates the position of each entity and draws it onto the screen
    def Update(self,screen):
        for entity in self.entityList:
            entity.Update()
            pygame.draw.rect(screen, entity.color, entity.GetRect())
       
    #Draws each entity onto the screen 
    def DrawEntities(self, screen):
        for entity in self.entityList:
            pygame.draw.rect(screen, entity.color, entity.GetRect())
        
    
    #Adds an entity if not in the list
    def AddEntity(self, newEntity:ObjectEntety):
        if self.ContainsEntity(newEntity):
            print("Have Entity")
            return
        
        print(f"Added Entity: {newEntity.name}")
        self.entityList.append(newEntity)
        
    #Removes the entity if not in the list
    def RemoveEntity(self, entity):
        entityIndex = self.GetEntityIndex(entity)
        
        if entityIndex == -1:
            return
        
        self.entityList.pop(entityIndex)
    
    #Checks if the entity collides with any other entity
    def DoesEntityCollide(self, mainEntity:ObjectEntety):
        if self.ContainsEntity(mainEntity) == False:
            return False
        
        for entity in self.entityList:
            if entity.id == mainEntity.id:
                continue
            
            if mainEntity.ShouldCheckCollision(entity) == False:
                continue
            
            print(f"Checking Collision Between {mainEntity.name} and {entity.name}")
            
            if mainEntity.IsColliding(entity):
                return True
            
        return False
    
    #Gets the index of the entity in the list, if not found return -1
    def GetEntityIndex(self, newEntity):
        i = 0
        for foundEntity in self.entityList:
            if foundEntity.id == newEntity.id:
                return i
            i = i + 1
        return -1
    
    
    #Checks if the entity is in the entity list
    def ContainsEntity(self, entity):
        return self.GetEntityIndex(entity) != -1
