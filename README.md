# eve_fits_itemiser
Itemises fits for EVE Online

We get a set of fits and we format it for things :)
It uses a .order file to get instructions on what fits to collate, which are then collected, formatted and then collated into a... .order file (fun naming system).

Test Alliance Best Alliance!

** Instructions for basic use **

1. Git clone this
2. Get some fits that follow the hyena.fit
3. Run 'python eve_fits_itemiser_main.py <*.order file you are using>'
   The format for a *.order file is <$relative path from dir running python $quantity> -----> ./fits/hyena.fit 30
4. Get collated fit results that all those fits require from final_order.ord.order
5. ????
6. Profit!!1


** Project Requirements **

CANCEL Get fits from a .fit file ---> organised .item_fit file ---> There is no .item_fit
DONE Orders are compiled into a .order file and comprise of all
DONE Orders can be formatted to have T2 items at the top and faction/meta at the bottom so manufacturers don't scream when sorting through it

DONE It has to translate fits to itemised module lists
DONE Itemised fits must be used to get total orders
DONE An order uses itemised fits and a quantity associated with that
DONE Each fit has a list of modules - their name and the number required
DONE Each order has a list of modules required, their name and the number required from every fit * quantity required

DONE The .fit is manually made by a user.  Sorry!

TODO Order lists should include price (somehow)
TODO Order lists should be exportable to Trello (if possible)

