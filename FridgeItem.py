"""
Created on Nov 8, 2020

@author: ssmup
"""
import datetime

class FridgeItem(object):
    """
    FridgeItem
        fields:
            str[] name
            str[] type (general category; dairy, vegetable, etc.)
            Date[] date_obtained
            Date[] expiry
            float[] quantity (unitless)
            str[] quantity_units
            (the first value in the array is the current value, the second is the most recent, third is second=most recent, etc. tracks modifications)
            boolean trackChanges    NOTE: removed this. it's pointless.
            
        functions:
            -constructor (all fields required, some can be blank)
            -getters
            -setters (have sanitization)
            -is_expired
    """
    

    def __init__(self, name, quantity, quantity_units, date_obtained = datetime.date.today(), expiry_date=None):
        """
        The constructor will default the expiry date to None, and the date_obtained to today, but requires the name, quantity, and quantity units of the item.
        """
        #fields are stored as arrays, where the first value in the array is the current value, the second is the most recent, third is second-most recent, etc.
        #fields are stored this way to store old values in order to be able to preserve the history of values/track changes
        
        self._name = [];
        self._quantity = [];
        self._quantity_units = [];
        self._date_obtained = [];
        self._expiry = [];
        
        name = name.strip();
        quantity_units = quantity_units.strip();
        self._name.insert(0, name);
        self._quantity.insert(0, quantity);
        self._quantity_units.insert(0, quantity_units);
        self._date_obtained.insert(0, date_obtained);
        self._expiry.insert(0, expiry_date);
        
    @property
    def name(self):
        """
        Name of the item.
        """
        return self._name[0];
    @name.setter
    def name(self, new_name):
        new_name = new_name.strip();
        self._name.insert(0, new_name);
        self._field_trimmer(self._name);
        
    @property
    def date_obtained(self):
        """
        The date the item was obtained. Datetime object.
        """
        return self._date_obtained[0];
    @date_obtained.setter
    def date_obtained(self, new_date_obtained):
        self._date_obtained.insert(0, new_date_obtained)
        self._field_trimmer(self._date_obtained);
        
    @property
    def expiry(self):
        """
        The expiry date of the item. Datetime object.
        """
        return self._expiry[0];
    @expiry.setter
    def expiry(self, new_expiry_date):
        self._expiry.insert(0, new_expiry_date)
        self._field_trimmer(self._expiry);
    
    @property
    def quantity(self):
        """
        Quantity of the item. float.
        """
        return self._quantity[0];
    @quantity.setter
    def quantity(self, new_quantity):
        new_quantity = abs(new_quantity);   #you can't have negative items in your fridge.
        self._quantity.insert(0, new_quantity);
        self._field_trimmer(self._quantity)
    @property
    def quantity_units(self):
        """
        Units of the quantity of the item. String.
        """
        return self._quantity_units[0];
    @quantity_units.setter
    def quantity_units(self, new_quantity_units):
        new_quantity_units = new_quantity_units.strip();
        self._quantity_units.insert(0, new_quantity_units);
        self._field_trimmer(self._quantity_units);
    
    def _field_trimmer(self, field, max_length=5):
        """
        If the passed field is storing more than max_length entries, trim it down to only max_length entries.
        max_length is defaulted to 5. Don't plan on changing that.
        Prevents fields from getting too long and unwieldy to deal with.
        """
        length = len(field);
        while(length > max_length):
            #print("Field trimmer field: ",field,"\nField length: ", length);
            field.pop();
            length = len(field);
            
    def is_expired(self):
        """
        Compares the current date to the expiry field, returning 1 if the expiry date is in the past, 0 if the expiry date is in the future, and -1 if this item does not have an expiry date..
        """
        current_date = datetime.date.today();
        is_expired = -1;
        if(self.expiry is not None):
            if(self.expiry - current_date < datetime.timedelta(microseconds=0)):
                is_expired = 1;
            else:
                is_expired = 0;
        return is_expired;
    
    def get_days_until_expiration(self):
        """
        Returns an int of the amount of days until the expiration date. 
        Returns None if no expiration date exists for this item, and negative days if already expired.
        """
        current_date = datetime.date.today();
        days_until_expiration = None;
        if(self.expiry is not None):
            time_difference = self.expiry - current_date;
            days_until_expiration = time_difference.days;
        return days_until_expiration;
            
    def __str__(self):
        """
        Basic string representation of the FridgeItem.
        """
        return "Name: " + str(self.name) + " Quantity: " + str(self.quantity) + " " + self.quantity_units + " Expiration Date: " + str(self.expiry);
            
    