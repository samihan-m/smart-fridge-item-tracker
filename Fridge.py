"""
Created on Nov 3, 2020

@author: ssmup

Organization plan:

    Fridge (runner)
        fields:
            -FridgeItem itemList
        

        functions:
            -main (contains the Kivy GUI)
            -addItem
            -removeItem
            -modifyItem
    
    FridgeItem
        fields:
            str[] name
            str[] type (general category; dairy, vegetable, etc.)
            Date[] expiry
            Date[] date_obtained
            int[] quantity (unitless)
            (the first value in the array is the current value, the second is the most recent, third is second=most recent, etc. tracks modifications)
            boolean trackChanges
            
        functions:
            -constructor (all fields required, some can be blank)
            -getters
            -setters (have sanitization)
"""
from FridgeItem import FridgeItem

class Fridge(object):
    
    def __init__(self):
        """
        Initializes an empty item list.
        """
        self.item_list = [];
        
    def add_item(self, item_to_add):
        """
        Adds a FridgeItem to this Fridge's item_list.
        """
        self.item_list.append(item_to_add);
        
    def remove_item_by_index(self, index_of_item_to_remove):    #when browsing through the item list, the browser will know what index is selected, and pass that to this.
        """
        Removes the FridgeItem at this index within the Fridge's item_list
        """
        self.item_list.pop(index_of_item_to_remove);
        
    def modify_item_by_index(self, index_of_item_to_modify, modified_item):  #when browsing through the item list, the browser will know what index is selected, and pass that to this.
        """
        Modifies the FridgeItem at this index by replacing it with a new FridgeItem with the new information.
        """
        self.item_list[index_of_item_to_modify] = modified_item;

    def _testcases(self):
        """
        Test cases for the Fridge. Don't call this.
        """
        item = FridgeItem("xd");
        print(item.name);           #testing item instantiation
        
        for i in range(1,10):       #testing field_trimmer
            item.quantity = i+1;
            print(item._quantity);
            
        for i in range(1,10):       #testing if -= works with the @property getter
            item.quantity -= 1;
            print(item._quantity);
        #continue with testing here..
            
    if __name__ == '__main__':
        from Fridge import Fridge
        fridge = Fridge();
        
        #comment this out if i want to avoid testcases
        fridge._testcases();
        
        #TODO: make the gui :DDD
                
        pass
    
    