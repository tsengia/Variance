// Variance API Unit Library
class Unit extends VarianceObject {
	
	static _endpoint = "units/";
	
	static search_by_name(name, count=20, offset=0) {
		// Should return a list of Unit objects from the response
		return [];
	}

	constructor(name, abbreviation, dimension, multiplier) {
		this.name = name;
		this.description = "";
		this.dimension = dimension;
		this.multiplier = multiplier;
		// NOTE: Removable units cannot be created via webapi, must be done through CLI
	}
}
