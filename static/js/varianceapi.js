// Variance API Library
class VarianceObject {
	
	static get_from_id(objecttype, id) {
		// Should return an object of type objectype if a valid response is received
		
	}
	
	remove() { 
		// Attempts to delete the object from the DB
	}
	
	push() { 
		// Attempts to update the object in the DB
	}
	
	refresh() { 
		// Attempts to update the object (locally) based on data from the DB.
		// Basically just does a get_from_id with the already existing ID
	}
	
	get id() {
		return this._id;
	}
	
	set id(new_id) {
		console.error("You cannot manually set a VarianceObject ID!");
		return False;
	}
	
	constructor() {
		this._id = null;
	}
}