'''
Created on Nov 9, 2020
This is going to be the runner as well as where all of the GUI stuff will be.

@author: ssmup
'''
import kivy
kivy.require("1.11.1");

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

from kivy.config import Config

import datetime

from Fridge import Fridge
from FridgeItem import FridgeItem

import pickle

#global so i can save and load from it outside of the ItemDisplay
fridge = Fridge();
#global so i can reference it within the ItemDisplay
file_directory = "item_list.txt";

class ItemDisplay(GridLayout):
    '''
    TODO:
    format buttons!!!
        -expiry date buttons mainly
                                                        add good font
                                                        add variable reading from Item Name, Quantity (Number) and Quantity (Units)
                                                            -> then use that to make a new FridgeItem
                                                                ->check if the item is valid by checking all 6 variables
                                                        ^DONE
                                                        make inputting text not make user have to backspace everything, 
    and potentially make it all reset after clicking add item.
    
    add pop up keyboard when clicking on text areas (maybe already done?)
    
                                                        confirm item deletion
    
                                                        make each item button have a border color that is green if not expired, yellow if within a day or two of expiring, red if expired, 
                                                            and white (?) if no expiration date was etnered
    
    ---
                                                        figure out date comparison for expiry dates
                                                        delete items from list (open popup when selecting a button? maybe the popup has a delete button with all the detailed info)
    figure out how to get pictures for items
                                                        edit item button in the Item popup
                                                        
                                need to figure out how to update item popups immediately after user clicks edit (the popup user returns to is incorrect)
                                    ->i added a little info label to tell the user that they need to re-open the item to see updated information.
                                        if i can figure out how to fix it, do that, but this is fine.
    
    add new markers for different things (low on quantity, custom marker by user, etc.)
    add custom marking system
    
                                                        fix scrolling to see all of the items
                                                        
    add a login screen with password?
    
                                                        make it so that unless year and month are selected, the day button is disabled. (either visually via color, or actually disabled)
    
    things to add to FridgeItem:
                                                        quantity units (string)
                                                        date obtained (datetime object)
                                                        -> figure out which variables are going to be optional    
    
    
    '''

    def __init__(self, **kwargs):
        super(ItemDisplay, self).__init__(**kwargs);
        #self.orientation = 'vertical';
        self.cols = 1;
        #self.fridge = Fridge();
        
        #setting new item fields
        self.new_item_day = None;
        self.new_item_month = None;
        self.new_item_year = None;
        self.new_item_name = None;
        self.new_item_quantity = None;
        self.new_item_quantity_units = None;
        
        #setting up keyboard pop-up
        Config.set('kivy', 'keyboard_mode', 'systemandmulti');
        
        #adding test items
        """
        for i in range(10):
            x = FridgeItem("Item" + str(i));
            self.fridge.add_item(x);
        """
            
        scroller = ScrollView();
        self.button_box = GridLayout(cols = 2, padding = 5, size_hint_x = 1, size_hint_y = None); #made this self. so i can affect it in reload_item_selectors
        self.button_box.bind(minimum_height=self.button_box.setter('height'));
        scroller.add_widget(self.button_box);
        
        add_item_button = Button(text="Add Item!", size_hint_y = None, font_size="25sp");
        add_item_button.bind(on_press=self.add_item_popup);
        self.add_widget(add_item_button);
        #contents of add_item_popup used to be here
        
        #generating buttons for each item on the list
        self.reload_item_selectors();
        
        #item label
        item_label = Label(text="Items: (Try scrolling up and down!)", size_hint_y = None, font_size="20sp");
        self.add_widget(item_label);
        
        self.add_widget(scroller);
        
    def reload_item_selectors(self):
        """
        Clears all buttons, then scans through the fridges' item_list and adds a button for each item.
        """
        self.button_box.clear_widgets();
        i = 0;
        for item in fridge.item_list:
            button = Button(text=item.name + " - " + str(item.quantity) + " " + str(item.quantity_units), size_hint_y = None, font_size = "25sp");
            button.id = str(i);
            button.bind(on_press=self.item_button_callback);
            days_until_item_expiry = item.get_days_until_expiration();
            button.background_color = (0.8, 0.8, 0.8, 1); #make item buttons with no Expiry value gray
            if(days_until_item_expiry is not None):
                if(days_until_item_expiry < 0):
                    button.background_color = (1, 0, 0, 1); #item expired, make it red
                elif(days_until_item_expiry > 0 and days_until_item_expiry < 3):
                    button.background_color = (1, 1, 0, 1); #item expires soon, make it yellow
                else:
                    button.background_color = (0, 1, 0, 1); #item not expiring soon, make it green
            self.button_box.add_widget(button);
            i += 1;
        
            
    def item_button_callback(self, button):
        """
        Triggers when user selects an item button.
        Loads a popup with specific item details as well as showing a Delete button.
        """
        item = fridge.item_list[int(button.id)];
        popup_pane = BoxLayout(orientation="vertical");
        name_label = Label(text=item.name);
        quantity_label = Label(text=str(item.quantity) + " " + item.quantity_units);
        date_obtained_label = Label(text="Obtained on " + str(item.date_obtained));
        expiry_label = Label(text="Expiration date: " + str(item.expiry));
        date_explanation_label = Label(text="Dates are YY/MM/DD");
        
        #days until expiry label
        days_until_item_expiry = item.get_days_until_expiration();
        add_days_until_expiry_label = False;
        if(days_until_item_expiry is not None):
            #expiration message
            add_days_until_expiry_label = True;
            days_until_expiry_label = Label(text = str(days_until_item_expiry) + " days left", font_size="25sp");
            if(days_until_item_expiry < 0):
                #already expired message
                days_until_expiry_label.text = "Expired " + str(abs(days_until_item_expiry)) + " days ago!";
                days_until_expiry_label.color = (1, 0, 0, 1);   #item expired, make it red
            elif(days_until_item_expiry > 0 and days_until_item_expiry < 3):
                days_until_expiry_label.color = (1, 1, 0, 1);   #item expires soon, make it yellow
            else:
                days_until_expiry_label.color = (0, 1, 0, 1);   #item not expiring soon, make it green
        
        """    part of old expiry label
        expired_code_dict = {
            -1: "No Expiry Date Entered",
            0: "Not Expired",
            1: "Expired!"
            };
        
        expired_code = item.is_expired();
        expired = expired_code_dict.get(expired_code);
        
        expired_label= Label(text="Expired?: " + str(expired));
        """
        
        
        item_delete_button = Button(text="Delete this Item", id=button.id); #passing button id (item index) to the delete callback
        #item_delete_button.bind(on_press=self.delete_item_callback);
        item_delete_button.bind(on_press=self.delete_item_confirm);
        popup_pane.add_widget(item_delete_button);
        
        popup_pane.add_widget(name_label);
        popup_pane.add_widget(quantity_label);
        popup_pane.add_widget(date_obtained_label);
        popup_pane.add_widget(expiry_label);
        """    part of old expiry label
        if(expired_code > -1):     #hiding the expired label if no expiration date was entered
            popup_pane.add_widget(expired_label);
        """
        if(add_days_until_expiry_label):
            popup_pane.add_widget(days_until_expiry_label);
            
        popup_pane.add_widget(date_explanation_label);
            
        #edit item button
        item_edit_button = Button(text="Edit this Item", id=button.id);
        item_edit_button.bind(on_press=self.edit_item_popup);
        popup_pane.add_widget(item_edit_button);
        
        popup_close_button = Button(text="Close");
        popup_pane.add_widget(popup_close_button);
        
        popup = Popup(title="Fridge Item Information", content=popup_pane, size_hint=(0.6,0.6));
        popup_close_button.bind(on_press=popup.dismiss);
        item_delete_button.bind(on_release=popup.dismiss);
        
        popup.open();
    
    def generate_item_detail_popup(self, item_index=None):
        """
        The popup used by add_item_popup and edit_item_popup. Abstracts the code so I don't write it twice.
        If item_id is None, then this function will produce the add_item_popup.
        If item_id is defined, then this function will autofill the fields of the popup with the item details.
        """
        
        #add item panel
        popup_pane = GridLayout(cols = 1, padding=10); #1 column. everything will be stacked.
        
        
        name_input_pane = BoxLayout(orientation="horizontal");  #label then textinput
        quantity_number_input_pane = BoxLayout(orientation="horizontal");  #label then textinput
        quantity_units_input_pane = BoxLayout(orientation="horizontal");  #label then textinput
        
        popup_pane.add_widget(name_input_pane);
        popup_pane.add_widget(quantity_number_input_pane);
        popup_pane.add_widget(quantity_units_input_pane);
        
        
        #The name input row
        name_input_label = Label(text="Item Name: ");
        name_input_text_input = TextInput(text="", multiline=False, font_size="30sp", halign= "center");
        name_input_text_input.bind(text=self.name_input_callback);
        
        
        name_input_pane.add_widget(name_input_label);
        name_input_pane.add_widget(name_input_text_input);
        
        
        #The quantity number input row
        quantity_number_input_label = Label(text="Quantity Number: (Can be decimal, e.g. 4, 12, 1.5, etc.)");
        quantity_number_input_text_input = TextInput(text="", input_filter="float", multiline=False, font_size="30sp", halign= "center");
        quantity_number_input_text_input.bind(text=self.quantity_input_callback);
        
        quantity_number_input_pane.add_widget(quantity_number_input_label);
        quantity_number_input_pane.add_widget(quantity_number_input_text_input);
        
        
        #The quantity units input row
        quantity_units_input_label = Label(text="Quantity Units: (A word or two, e.g. cartons, ounces, etc.)");
        quantity_units_input_text_input = TextInput(text="", multiline=False, font_size="30sp", halign= "center");
        quantity_units_input_text_input.bind(text=self.quantity_units_input_callback);
        
        quantity_units_input_pane.add_widget(quantity_units_input_label);
        quantity_units_input_pane.add_widget(quantity_units_input_text_input);
        
        #expiry date optional label
        add_item_expiry_row_label = Label(text="Optional: (select none or all 3)");
        popup_pane.add_widget(add_item_expiry_row_label);
        
        #expiry date row (month: day: year: ; a row of 3 cols of text entries)
        add_item_expiry_date_pane = GridLayout(cols = 3);
        popup_pane.add_widget(add_item_expiry_date_pane);
        
        #expiry month
        months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");
        add_item_expiry_month_input = Spinner(text="Month", values=months);
        add_item_expiry_month_input.bind(text=self.month_input_callback);   #triggers a callback whenever a value is selected
        add_item_expiry_date_pane.add_widget(add_item_expiry_month_input);
        
        #expiry day
        self.days = ("Day - Pick a month first", "If you want February 29,", "pick a leap year first"); #set blank by default, updates when month is selected
        self.add_item_expiry_day_input = Spinner(text="Day", values=self.days); #made self. to target from day_update_on_month_input
        self.add_item_expiry_day_input.bind(on_press=self.day_update_callback); #updating day list whenever user clicks on it
        self.add_item_expiry_day_input.bind(text=self.day_input_callback);      #saving day value user selects
        self.add_item_expiry_day_input.color = (0, 0, 0, 0.2);      #making the day color dark as if it's disabled
        self.add_item_expiry_day_input.disabled = True;             #actually disabling the button
        add_item_expiry_date_pane.add_widget(self.add_item_expiry_day_input);
        
        #expiry year
        #generating year options
        right_now = datetime.date.today();
        current_year = right_now.year;
        #print(current_year);
        year_gen = [];
        year_range = 15; #giving a range of now to 15 years from now.
        for i in range(0, year_range + 1):     
            year_gen.append(str(current_year + i));
        years = tuple(year_gen);
        
        add_item_expiry_year_input = Spinner(text="Year", values=years);
        add_item_expiry_year_input.bind(text=self.year_input_callback);
        add_item_expiry_date_pane.add_widget(add_item_expiry_year_input);
        
        #date input info label
        date_input_info_label = Label(text="To make things easy, first enter Year, then Month, then Day.");
        popup_pane.add_widget(date_input_info_label);
        
        #resetting date variables because they persist through item creation
        self.new_item_day = None;
        self.new_item_month = None;
        self.new_item_year = None;
        
        #Add Item button
        add_item_button = Button(text="Add Item!", size_hint_y = None, font_size="25sp");   #default is 15sp
        add_item_button.bind(on_press=self.save_item);
        popup_pane.add_widget(add_item_button);
        
        popup = Popup(title="Add an Item", content=popup_pane);
        #add_item_button.bind(on_release=popup.dismiss);
        
        #add popup close button
        popup_pane_close_button = Button(text="Cancel");
        popup_pane_close_button.bind(on_press=popup.dismiss);
        popup_pane.add_widget(popup_pane_close_button);
        
        #autofilling - this is an edit popup
        if(item_index is not None):
            popup.title = "Edit an Item";
            
            item = fridge.item_list[int(item_index)];   #the id is actually the index of the item in the item list
            name_input_text_input.text = item.name;
            quantity_number_input_text_input.text = str(item.quantity);
            quantity_units_input_text_input.text = item.quantity_units;
            
            expiry_date = item.expiry;
            if(expiry_date is not None):
                month = expiry_date.month;
                month_str = months[month-1]; #subtracting 1 because the index of january is 0 (value of january is 1)
                day = expiry_date.day;
                year = expiry_date.year;
                add_item_expiry_year_input.text = str(year);
                add_item_expiry_month_input.text = month_str;
                self.add_item_expiry_day_input.disabled = False;    #enabling the day button for items who already have a day value
                self.add_item_expiry_day_input.text = str(day);
                
            
            add_item_button.text = "Save Item Changes!";
            add_item_button.id = item_index;   #passing item index so it can be used by save_item
            add_item_button.bind(on_press=self.save_item);
            
        return popup;
        
        
    def add_item_popup(self, button):
        """
        When the Add Item button is pressed, show a popup with TextInputs and another button to add it, with another button to cancel.
        """
        
        popup = self.generate_item_detail_popup();
        popup.open();
        
        
    def delete_item_confirm(self, button):
        """
        Pops up a "Are you sure?" prompt which the user must accept to delete the item.
        """
        confirmation_popup_pane = BoxLayout(orientation="vertical");
        
        confirmation_label = Label(text="Are you sure?");
        
        options_pane = GridLayout(cols = 2);
        yes_button = Button(text="Yes", id=button.id);  #passing the item id to delete_item_callback
        no_button = Button(text="No");
        options_pane.add_widget(yes_button);
        options_pane.add_widget(no_button);
        
        confirmation_popup_pane.add_widget(confirmation_label);
        confirmation_popup_pane.add_widget(options_pane);
        
        confirmation_popup = Popup(title="Delete this Item", content=confirmation_popup_pane, size_hint=(0.5, 0.5));
        no_button.bind(on_press=confirmation_popup.dismiss);
        yes_button.bind(on_press=self.delete_item_callback);
        yes_button.bind(state=confirmation_popup.dismiss);
        
        confirmation_popup.open();
        
    def delete_item_callback(self, button):
        """
        Triggered when user selects the Delete button in an Item popup and confirms the deletion.
        Deletes the item from the fridge's item_list, then reloads buttons.
        """
        item_index = int(button.id);
        fridge.item_list.pop(item_index);
        self.reload_item_selectors();
    
    
    def save_item(self, button):
        """
        Checks validity of the 6 new_item variables. If any are invalid, show a popup detailing the error.
        Otherwise, create the new_item.
        If an item_index is not specified within button.id, add it to the fridge.item_list.
        Otherwise, set the item at the specified index to this new item.
        """
        #first, check if all variables are defined. then create the fridge item and add it.
        errors = [];
        if(self.new_item_name is None or self.new_item_name == ""):
            errors.append("Name");
        if(self.new_item_quantity is None):
            errors.append("Quantity");
        if(self.new_item_quantity_units is None or self.new_item_quantity_units == "" or self.new_item_quantity_units == "Quantity (Units)"):    #need this special check because the quantity units is set to Quantity (Units) by default for some reason
            errors.append("Quantity Units");
        #not error checking date vars because they're optional
        """
        if(self.new_item_month is None):
            errors.append("Month");
        if(self.new_item_day is None):
            errors.append("Day");
        if(self.new_item_year is None):
            errors.append("Year");
        """
        
        if(len(errors) > 0):            #errors - not all vars were properly defined. open a popup showing which were wrong.
            error_message = ", ".join(errors);
            error_label = Label(text="Invalid: " + error_message);
            popup_close_button = Button(text="Close this popup");
            popup_pane = BoxLayout(orientation = "vertical");
            popup_pane.add_widget(error_label);
            popup_pane.add_widget(popup_close_button);
            
            error_popup = Popup(title="Invalid Item Entry", content=popup_pane, size_hint=(0.6,0.6));   #size_hint resizes popup
            popup_close_button.bind(on_press=error_popup.dismiss);
            error_popup.open();
        else:                           #continue with adding item
            if(self.new_item_month is None or self.new_item_day is None or self.new_item_year is None): #if any part of the date is invalid, don't create a datetime object.
                expiry = None;
            else:                   #if every part of the date entry is valid, then make a datetime object and use that.
                expiry = datetime.date(self.new_item_year, self.new_item_month+1, self.new_item_day);   #month is +1 because i need to go from 0..11 to 1..12  
                
            item = FridgeItem(self.new_item_name, expiry_date= expiry, quantity= self.new_item_quantity, quantity_units= self.new_item_quantity_units);
            
            success_popup_pane = BoxLayout(orientation="vertical");
            success_label = Label(text="Item added successfully! Exit the Add Item Menu.");
            success_popup_pane.add_widget(success_label);
            success_popup_close_button = Button(text="Close", size_hint_y = None);
            success_popup_pane.add_widget(success_popup_close_button);
            
            success_popup = Popup(title="Success!", content=success_popup_pane, size_hint=(0.6,0.6));
            success_popup_close_button.bind(on_press=success_popup.dismiss);
            
            print_log = "Item added: %s";
            
            if(button.id is None):
                fridge.add_item(item);
            else:
                item_index = int(button.id);
                fridge.item_list[item_index] = item;
                success_label.text = "Item added successfully! Exit the Edit Item Menu.\nChanges won't be updated until you \nclose the Item Information Menu and re-open it.";
                print_log = "Item changed: %s";
                
            print(print_log % item);
            success_popup.open();
            
            
            self.reload_item_selectors();
            
    def edit_item_popup(self, button):
        """
        Triggers whenever the user selects the Edit Item option within the item button popup.
        Opens the edit_item popup.
        """
        popup = self.generate_item_detail_popup(button.id); #passing id to the generator so it autofills with the item's details
        popup.open();
    
    def name_input_callback(self, text_input, text):
        """
        Triggers whenever the new item name TextInput receives new input.
        Saves the input to a variable, self.new_item_name.
        """
        self.new_item_name = text;
        print("New Item Name updated: %s" % text);
        
    def quantity_input_callback(self, text_input, text):
        """
        Triggers whenever the new item quantity TextInput receives new input.
        If the input is a float, save it.
        """
        if(text == ""):
            self.new_item_quantity = None;  #making a blank text field set the quantity to None, it makes more sense
            print("New Item Quantity reset: %s" % str(self.new_item_quantity));
            return;
        try:
            float(text);
        except:
            return;
        else:
            self.new_item_quantity = float(text);
            print("New Item Quantity updated: %s" % text);
        
    def quantity_units_input_callback(self, text_input, text):
        """
        Triggers whenever the new item quantity units TextInput receives new input.
        Saves the input to a variable, self.new_item_quantity_units.
        """
        self.new_item_quantity_units = text;
        print("New Item Quantity Units updated: %s" % text);
        
    def month_input_callback(self, spinner, text):
        """
        Triggers whenever user selects a different month on the month drop down.
        Sets self.month value.
        """
        month_day_count = {
            "January": 31,
            "February": 28,
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31,
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31
            };
        self.new_item_month = int(list(month_day_count.keys()).index(text));    #turning dict keys into a list and scanning it for the month number of the input text
        day_count = month_day_count.get(text)
        days_gen = [];
        for i in range(1, day_count+1):
            days_gen.append(str(i));
        days = tuple(days_gen);
        self.days = days;
        self.day_update_on_date_input();        #resets day selection on month select
        self.day_range_update_on_date_input();  #calls function to attempt leap year check
        spinner.color = (0, 1, 0, 1);       #makes the spinner green
        print("Month selected: %d" % self.new_item_month);
        
    def day_range_update_on_date_input(self, *args):
        """
        Triggers whenever user selects a year/month.
        If the month selected is February, adds 29 to February's day options on leap years.
        Also, if the selected day is February 29 and the user switches off of a leap year, the selected day switches to February 28.
        """
        #checks if year and month are selected. if so, run leap year check.
        if(self.new_item_year is not None and self.new_item_month is not None):
            if(self.new_item_year % 4 == 0 and self.new_item_month == 1):   #1 = index of february
                days_list = list(self.days);
                days_list.append("29");    #adds 29 as a day option in February to leap years.
                self.days = tuple(days_list);
                print("Leap year day added.");
            elif(self.days[len(self.days)-1] == "29"):
                self.days = self.days[:-1]; #removes 29 when returning to non-leap years
                if(self.add_item_expiry_day_input.text == "29"):
                    self.add_item_expiry_day_input.text = "28"; #automatically unsetting day from 29 if switching away from a leap year.
    
    def day_update_on_date_input(self, *args):
        """
        Triggers whenever user selects a month. 
        Resets the day so that no issue where the day doesn't exist for that month occurs. (e.g. Feb 31)
        """
        self.add_item_expiry_day_input.color = (1, 1, 1, 1);    #making the day button color white, as if enabling it
        self.add_item_expiry_day_input.disabled = False;        #actually enabling the button
        self.new_item_day = None;   #undefine day because it needs to be re-picked
        print("Reset selected day.");
        
    def day_update_callback(self, instance):
        """
        Triggers whenever user clicks on the Days spinner. Updates the options and resets the selected option.
        """
        instance.values = self.days;
        days_length = len(self.days);
        #print(days_length);
        print(self.days);
        if(days_length > 2): #checking if self.days holds the range of days instead of just "Pick a month"
            if(instance.text.isnumeric()):
                if(int(instance.text) > int(self.days[days_length-1])):    #resets day so if I switch from March to February and I selected 30 it switches to the new max as a sort of error protection,
                    instance.text = self.days[days_length-1];
        print("Day menu updated");
        
    def day_input_callback(self, spinner, text):
        """
        Triggers whenever user selects a day.
        Sets self.day value.
        """
        if(text.isnumeric()):       #if the day isn't a number, dont save it
            self.new_item_day = int(text);
            spinner.color = (0, 1, 0, 1);       #makes the spinner green
            print("Day selected: %d" % self.new_item_day);
        
    def year_input_callback(self, spinner, text):
        """
        Triggers whenever user selects a year. 
        Sets self.year value.
        Checks if the year is divisible by 4. If so, and the month selected is February, reset the day value and change it's range to 1-29.
        The spinner becomes green once the user selects an option.
        """
        self.new_item_year = int(text);
        self.day_range_update_on_date_input(); #calls function to attempt leap year check
        spinner.color = (0, 1, 0, 1);       #makes the spinner green
        print("Year selected: %d" % self.new_item_year);

class FridgeApp(App):
    """
    classdocs
    """
    def build(self):
        return ItemDisplay();
        
if __name__ == '__main__':
    
    #load fridge items here
    try:
        with open(file_directory, "rb") as file_input:
            item_list = pickle.load(file_input);
            fridge.item_list = item_list;
            print("Items loaded:");
            print(', '.join(map(str, item_list)));
    except Exception as e:
        print("Error occurred while loading items.");
        print(e);
        
    app = FridgeApp();
    app.run();
    
    #save fridge items here
    try:
        with open(file_directory, "wb") as file_output:
            item_list = fridge.item_list;
            pickle.dump(item_list, file_output, pickle.HIGHEST_PROTOCOL);
            print("Items saved:");
            print(', '.join(map(str, item_list)));
    except Exception as e:
        print("Error occurred while saving items.");
        print(e);