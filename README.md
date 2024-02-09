# Aventura ERP
Aventura ERP is a Commercial Management project. Here are the main functions in the "Purchase" module in the views.py file located at: apps/home/views.py.


The views.py file contains Django view functions for managing purchase requests, orders, and their approvals within the application. Below is an overview of each function:

1. send_demande(request)
This function handles the submission of purchase requests. It retrieves items from a list associated with the user, creates corresponding Demande objects, and then deletes the items from the list. After submission, it redirects the user to the add demand page.

2. edit_commande(request)
This function manages the submission of purchase orders. It retrieves items from a list associated with the user, creates corresponding Commande objects, sends an email notification for approval, and then redirects the user to the add command page.

3. approuver_dmd(request, id)
This function approves purchase requests identified by their unique identifier (id). It updates the status of specific lines associated with the request to mark them as approved and creates entries in the AprouvedAchat table for each supplier involved.

4. approuver_cmd(request, id)
This function approves purchase orders identified by their unique identifier (id). It updates the status of specific lines associated with the order to mark them as approved and creates an entry in the AprouvedAchat table.

5. refused_cmd(request, id)
This function handles the refusal of purchase orders identified by their unique identifier (id). It updates the status of specific lines associated with the order to mark them as refused and creates an entry in the RefusedAchat table.

6. grouper_cmd(request, id)
This function groups approved purchase orders based on the supplier. It updates the identifier of specific lines to group them under the same identifier, then redirects the user to the list of purchase orders.

7. annuler_cmd(request, id, identifier)
This function cancels refused purchase orders identified by their unique identifier (id). It deletes the refused order entry and associated lines.

8. delete_item_demande(request, id_item)
This function deletes a selected item from the purchase request form based on its unique identifier (id_item).

9. delete_item_commande(request, id_item)
This function deletes a selected item from the purchase order form based on its unique identifier (id_item).
