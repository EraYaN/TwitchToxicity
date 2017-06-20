String.prototype.isEmpty = function () {
	return (this.length === 0 || !this.trim());
};
String.prototype.isNumeric = function () {
	return !isNaN(parseFloat(this)) && isFinite(this);
}
Number.prototype.isNumeric = function () {
	return !isNaN(this) && isFinite(this);
}