# smart-fridge-item-tracker
 A touch-based interactive UI that keeps track of fridge items, storing name, quantity, and expiration date. Allows you to see everything in your fridge in one panel-based screen and modify any of those values at will. Designed to run on that screen that some smart fridges have on their door.
 
 Reads and stores data to a text file, saving upon the closing of the program. (A normal closing, not a crash.)
 
Uses Kivy to make a UI that I could port to Raspberry Pi and maybe put into a little screen I can glue onto the front of my fridge.

I heard this idea somewhere that if you design a UI for mobile use, it's useful because it allows you to use 1 interface for basically every device, instead of having to deal with a desktop version (potentially multiple desktop versions) and a mobile version, which I really liked. So, I wanted to use Kivy because I could design something for all devices at once. It's not like I would use this on multiple kinds of device, but I like that idea because it's like future-proofing a program you can make on your computer for porting to a mobile environment. Or something like that.

I wrote the fields for the FridgeItem class in a way that would track their change history, up to a previous 4 values. That was for an idea I had where editing an item would indicate to the user that it was modified, and show an option to show those previous values. I like that too, I think it's a cool way to track value history.
