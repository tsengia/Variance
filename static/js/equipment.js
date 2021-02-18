// Variance API Equipment Library
class Equipment extends VarianceObject {

	static _endpoint = "equipment/";
	
	static search_by_name(name, count=20, offset=0) {
		// Should return a list of Equipment objects from the response
		return [];
	}
	
	// Returns true if able to create new equipment object in database, false otherwise
	create() {
		if(this._id != null) {
			console.warn("Attempted to create Equipment object that already has an ID!");
			return false;
		}
		// Make request to create new equipment object in db
		
		return true;
	}
	
	constructor(name) {
		this.name = name;
		this.description = "";
	}
}
