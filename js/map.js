(function(){
"use strict";
function ՐՏ_extends(child, parent) {
    child.prototype = Object.create(parent.prototype);
    child.prototype.__base__ = parent;
    child.prototype.constructor = child;
}
function ՐՏ_Iterable(iterable) {
    var tmp;
    if (iterable.constructor === [].constructor || iterable.constructor === "".constructor || (tmp = Array.prototype.slice.call(iterable)).length) {
        return tmp || iterable;
    }
    return Object.keys(iterable);
}
function len(obj) {
    var tmp;
    if (obj.constructor === [].constructor || obj.constructor === "".constructor || (tmp = Array.prototype.slice.call(obj)).length) {
        return (tmp || obj).length;
    }
    return Object.keys(obj).length;
}
function range(start, stop, step) {
    var length, idx, range;
    if (arguments.length <= 1) {
        stop = start || 0;
        start = 0;
    }
    step = arguments[2] || 1;
    length = Math.max(Math.ceil((stop - start) / step), 0);
    idx = 0;
    range = new Array(length);
    while (idx < length) {
        range[idx++] = start;
        start += step;
    }
    return range;
}
function reversed(arr) {
    var tmp;
    tmp = arr.slice(0);
    return tmp.reverse();
}
function ՐՏ_type(obj) {
    return obj && obj.constructor && obj.constructor.name ? obj.constructor.name : Object.prototype.toString.call(obj).slice(8, -1);
}
function ՐՏ_eq(a, b) {
    var ՐՏitr13, ՐՏidx13;
    var i;
    if (a === b) {
        return true;
    }
    if (Array.isArray(a) && Array.isArray(b) || a instanceof Object && b instanceof Object) {
        if (a.constructor !== b.constructor || a.length !== b.length) {
            return false;
        }
        if (Array.isArray(a)) {
            for (i = 0; i < a.length; i++) {
                if (!ՐՏ_eq(a[i], b[i])) {
                    return false;
                }
            }
        } else {
            if (Object.keys(a).length !== Object.keys(b).length) {
                return false;
            }
            ՐՏitr13 = ՐՏ_Iterable(a);
            for (ՐՏidx13 = 0; ՐՏidx13 < ՐՏitr13.length; ՐՏidx13++) {
                i = ՐՏitr13[ՐՏidx13];
                if (!ՐՏ_eq(a[i], b[i])) {
                    return false;
                }
            }
        }
        return true;
    }
    return false;
}
var ValueError = (ՐՏ_8 = function ValueError() {
    ValueError.prototype.__init__.apply(this, arguments);
}, ՐՏ_extends(ՐՏ_8, Error), Object.defineProperties(ՐՏ_8.prototype, {
    __init__: {
        enumerable: true, 
        writable: true, 
        value: function __init__(message){
            var self = this;
            self.name = "ValueError";
            self.message = message;
        }
    }
}), ՐՏ_8);
var ՐՏ_modules = {};
ՐՏ_modules["stdlib"] = {};

(function(){
    var __name__ = "stdlib";
    var str;
    str = JSON.stringify;
    String.prototype.find = String.prototype.indexOf;
    String.prototype.strip = String.prototype.trim;
    String.prototype.lstrip = String.prototype.trimLeft;
    String.prototype.rstrip = String.prototype.trimRight;
    String.prototype.join = function(iterable) {
        return iterable.join(this);
    };
    String.prototype.zfill = function(size) {
        var s;
        s = this;
        while (s.length < size) {
            s = "0" + s;
        }
        return s;
    };
    function list(iterable) {
        var ՐՏitr1, ՐՏidx1;
        iterable = iterable === void 0 ? [] : iterable;
        var result, i;
        result = [];
        ՐՏitr1 = ՐՏ_Iterable(iterable);
        for (ՐՏidx1 = 0; ՐՏidx1 < ՐՏitr1.length; ՐՏidx1++) {
            i = ՐՏitr1[ՐՏidx1];
            result.append(i);
        }
        return result;
    }
    Array.prototype.append = Array.prototype.push;
    Array.prototype.find = Array.prototype.indexOf;
    Array.prototype.index = function(index) {
        var ՐՏ_1;
        var val;
        val = this.find(index);
        if ((val === (ՐՏ_1 = -1) || typeof val === "object" && ՐՏ_eq(val, ՐՏ_1))) {
            throw new ValueError(str(index) + " is not in list");
        }
        return val;
    };
    Array.prototype.insert = function(index, item) {
        this.splice(index, 0, item);
    };
    Array.prototype.pop = function(index) {
        index = index === void 0 ? this.length - 1 : index;
        return this.splice(index, 1)[0];
    };
    Array.prototype.extend = function(array2) {
        this.push.apply(this, array2);
    };
    Array.prototype.remove = function(item) {
        var index;
        index = this.find(item);
        this.splice(index, 1);
    };
    Array.prototype.copy = function() {
        return this.slice(0);
    };
    function dict(iterable) {
        var ՐՏitr2, ՐՏidx2;
        var result, key;
        result = {};
        ՐՏitr2 = ՐՏ_Iterable(iterable);
        for (ՐՏidx2 = 0; ՐՏidx2 < ՐՏitr2.length; ՐՏidx2++) {
            key = ՐՏitr2[ՐՏidx2];
            result[key] = iterable[key];
        }
        return result;
    }
    if (ՐՏ_type(Object.getOwnPropertyNames) !== "function") {
        dict.keys = function(hash) {
            var keys;
            keys = [];
            
        for (var x in hash) {
            if (hash.hasOwnProperty(x)) {
                keys.push(x);
            }
        }
        ;
            return keys;
        };
    } else {
        dict.keys = function(hash) {
            return Object.getOwnPropertyNames(hash);
        };
    }
    dict.values = function(hash) {
        var ՐՏitr3, ՐՏidx3;
        var vals, key;
        vals = [];
        ՐՏitr3 = ՐՏ_Iterable(dict.keys(hash));
        for (ՐՏidx3 = 0; ՐՏidx3 < ՐՏitr3.length; ՐՏidx3++) {
            key = ՐՏitr3[ՐՏidx3];
            vals.append(hash[key]);
        }
        return vals;
    };
    dict.items = function(hash) {
        var ՐՏitr4, ՐՏidx4;
        var items, key;
        items = [];
        ՐՏitr4 = ՐՏ_Iterable(dict.keys(hash));
        for (ՐՏidx4 = 0; ՐՏidx4 < ՐՏitr4.length; ՐՏidx4++) {
            key = ՐՏitr4[ՐՏidx4];
            items.append([key, hash[key]]);
        }
        return items;
    };
    dict.copy = dict;
    dict.clear = function(hash) {
        var ՐՏitr5, ՐՏidx5;
        var key;
        ՐՏitr5 = ՐՏ_Iterable(dict.keys(hash));
        for (ՐՏidx5 = 0; ՐՏidx5 < ՐՏitr5.length; ՐՏidx5++) {
            key = ՐՏitr5[ՐՏidx5];
            delete hash[key];
        }
    };
    ՐՏ_modules["stdlib"]["str"] = str;

    ՐՏ_modules["stdlib"]["list"] = list;

    ՐՏ_modules["stdlib"]["dict"] = dict;
})();

(function(){

    var __name__ = "__main__";

    var ՐՏ_2, ՐՏ_3, ՐՏ_4, ՐՏ_5;
    var WEEKLY_CAR_OWN_COST, OPACITY, GREY, COLORS, n, i, COLOR_SCALE, BINS, b, LABELS;
    var append = ՐՏ_modules["stdlib"].append;
    
    WEEKLY_CAR_OWN_COST = 2228 / 52;
    OPACITY = 1;
    GREY = "rgb(200, 200, 200)";
    COLORS = reversed([ "rgb(158,1,66)", "rgb(213,62,79)", "rgb(244,109,67)", "rgb(253,174,97)", "rgb(254,224,139)", "rgb(230,245,152)", "rgb(171,221,164)", "rgb(102,194,165)", "rgb(50,136,189)", "rgb(94,79,162)" ]);
    n = len(COLORS);
    COLOR_SCALE = d3.scale.linear().domain((function() {
        var ՐՏidx6, ՐՏitr6 = ՐՏ_Iterable(range(n)), ՐՏres = [], i;
        for (ՐՏidx6 = 0; ՐՏidx6 < ՐՏitr6.length; ՐՏidx6++) {
            i = ՐՏitr6[ՐՏidx6];
            ՐՏres.push(i / (n - 1));
        }
        return ՐՏres;
    })()).clamp(true).range(COLORS).interpolate(d3.interpolateHcl);
    BINS = [ null ].concat((function() {
        var ՐՏidx7, ՐՏitr7 = ՐՏ_Iterable(range(n)), ՐՏres = [], i;
        for (ՐՏidx7 = 0; ՐՏidx7 < ՐՏitr7.length; ՐՏidx7++) {
            i = ՐՏitr7[ՐՏidx7];
            ՐՏres.push(i / n);
        }
        return ՐՏres;
    })());
    LABELS = [ "n/a" ].concat((function() {
        var ՐՏidx8, ՐՏitr8 = ՐՏ_Iterable(BINS.slice(1)), ՐՏres = [], b;
        for (ՐՏidx8 = 0; ՐՏidx8 < ՐՏitr8.length; ՐՏidx8++) {
            b = ՐՏitr8[ՐՏidx8];
            ՐՏres.push((b * 100).toFixed(0) + "%");
        }
        return ՐՏres;
    })());
    var State = (ՐՏ_2 = function State() {
        State.prototype.__init__.apply(this, arguments);
    }, Object.defineProperties(ՐՏ_2.prototype, {
        __doc__: {
            enumerable: true, 
            writable: true, 
            value: "An object that holds the values of the user interface widgets."        },
        __init__: {
            enumerable: true, 
            writable: true, 
            value: function __init__(income, numBedrooms, numBedroomsRent, modes, commuteCosts, numWorkdays, parkingCosts, numCars, workAreaNames){
                var self = this;
                self.income = income;
                self.numBedrooms = numBedrooms;
                self.numBedroomsRent = numBedroomsRent;
                self.modes = modes;
                self.commuteCosts = commuteCosts;
                self.numWorkdays = numWorkdays;
                self.parkingCosts = parkingCosts;
                self.numCars = numCars;
                self.workAreaNames = workAreaNames;
            }
        },
        getWeeklyIncome: {
            enumerable: true, 
            writable: true, 
            value: function getWeeklyIncome(){
                var self = this;
                return self.income / 52;
            }
        },
        getWeeklyCarOwnCost: {
            enumerable: true, 
            writable: true, 
            value: function getWeeklyCarOwnCost(){
                var self = this;
                return self.numCars * WEEKLY_CAR_OWN_COST;
            }
        },
        getWeeklyParkingCost: {
            enumerable: true, 
            writable: true, 
            value: function getWeeklyParkingCost(){
                var self = this;
                var totalCost, k, parking, numWorkdays;
                totalCost = 0;
                for (k = 0; k < 2; k++) {
                    parking = self.parkingCosts[k];
                    numWorkdays = self.numWorkdays[k];
                    totalCost += parking * numWorkdays;
                }
                return totalCost;
            }
        },
        getWeeklyTotalCostFraction: {
            enumerable: true, 
            writable: true, 
            value: function getWeeklyTotalCostFraction(weeklyTotalCost){
                var self = this;
                var total, fraction;
                total = weeklyTotalCost;
                if (total !== null) {
                    fraction = total / self.getWeeklyIncome();
                } else {
                    fraction = null;
                }
                return fraction;
            }
        }
    }), ՐՏ_2);
    var AreaData = (ՐՏ_3 = function AreaData() {
        AreaData.prototype.__init__.apply(this, arguments);
    }, Object.defineProperties(ՐՏ_3.prototype, {
        __doc__: {
            enumerable: true, 
            writable: true, 
            value: "An object that holds data about rent and commute costs for each area.\nOnly one instance is needed."        },
        __init__: {
            enumerable: true, 
            writable: true, 
            value: function __init__(rentByNbedroomsByArea, MIndexByArea, M){
                var self = this;
                self.rentByNbedroomsByArea = rentByNbedroomsByArea;
                self.MIndexByArea = MIndexByArea;
                self.M = M;
            }
        },
        getWeeklyRent: {
            enumerable: true, 
            writable: true, 
            value: function getWeeklyRent(state, areaName){
                var self = this;
                var numBedrooms, numBedroomsRent, rent;
                numBedrooms = state.numBedrooms;
                numBedroomsRent = state.numBedroomsRent;
                rent = self.rentByNbedroomsByArea[areaName][numBedrooms];
                if (rent !== null) {
                    rent = parseFloat(rent);
                    rent *= parseInt(numBedroomsRent) / parseInt(numBedrooms);
                } else {
                    rent = null;
                }
                return rent;
            }
        },
        getWeeklyCommuteCostAndTime: {
            enumerable: true, 
            writable: true, 
            value: function getWeeklyCommuteCostAndTime(state, areaName){
                var ՐՏupk1, ՐՏupk2;
                var self = this;
                var totalCost, totalTime, i, k, numWorkdays, mode, workareaName, j, cost, time;
                totalCost = 0;
                totalTime = 0;
                if (state.workAreaNames === null) {
                    return [totalCost, totalTime];
                }
                i = self.MIndexByArea[areaName];
                for (k = 0; k < 2; k++) {
                    numWorkdays = state.numWorkdays[k];
                    if (!numWorkdays) {
                        continue;
                    }
                    mode = state.modes[k];
                    workareaName = state.workAreaNames[k];
                    if (workareaName === null) {
                        continue;
                    }
                    j = self.MIndexByArea[workareaName];
                    if (j > i) {
                        ՐՏupk1 = [ j, i ];
                        i = ՐՏupk1[0];
                        j = ՐՏupk1[1];
                    }
                    ՐՏupk2 = self.M[mode][i][j];
                    cost = ՐՏupk2[0];
                    time = ՐՏupk2[1];
                    if (cost === null) {
                        return [null, null];
                    } else {
                        cost += time * state.commuteCosts[k];
                    }
                    totalCost += numWorkdays * cost;
                    totalTime += numWorkdays * time;
                }
                return [totalCost, totalTime];
            }
        },
        getWeeklyTotalCost: {
            enumerable: true, 
            writable: true, 
            value: function getWeeklyTotalCost(state, areaName){
                var self = this;
                var rent, cc, total;
                rent = self.getWeeklyRent(state, areaName);
                cc = self.getWeeklyCommuteCostAndTime(state, areaName)[0];
                if (rent !== null && cc !== null) {
                    total = rent + cc + state.getWeeklyCarOwnCost() + state.getWeeklyParkingCost();
                } else {
                    total = null;
                }
                return total;
            }
        },
        getAreaStats: {
            enumerable: true, 
            writable: true, 
            value: function getAreaStats(state, areaName){
                var self = this;
                var wcct, wtc;
                wcct = self.getWeeklyCommuteCostAndTime(state, areaName);
                wtc = self.getWeeklyTotalCost(state, areaName);
                return {
                    "areaName": areaName,
                    "weeklyIncome": state.getWeeklyIncome(),
                    "weeklyRent": self.getWeeklyRent(state, areaName),
                    "numBedrooms": state.numBedrooms,
                    "numBedroomsRent": state.numBedroomsRent,
                    "weeklyCommuteCost": wcct[0],
                    "weeklyCommuteTime": wcct[1],
                    "weeklyParkingCost": state.getWeeklyParkingCost(),
                    "weeklyCarOwnCost": state.getWeeklyCarOwnCost(),
                    "weeklyTotalCost": wtc,
                    "weeklyTotalCostFraction": state.getWeeklyTotalCostFraction(wtc)
                };
            }
        }
    }), ՐՏ_3);
    var getState = (ՐՏ_4 = function getState(workAreaNames) {
        workAreaNames = workAreaNames === void 0 ? null : workAreaNames;
        var income, numBedrooms, numBedroomsRent, modes, commuteCosts, numWorkdays, parkingCosts, numCars;
        income = $("#income-slider").slider("value");
        numBedrooms = parseInt($("#num-bedrooms").val());
        numBedroomsRent = parseInt($("#num-bedrooms-rent").val());
        modes = [ $("#mode-y").val(), $("#mode-p").val() ];
        commuteCosts = [ $("#commute-cost-y-slider").slider("value"), $("#commute-cost-p-slider").slider("value") ];
        numWorkdays = [ $("#num-workdays-y-slider").slider("value"), $("#num-workdays-p-slider").slider("value") ];
        parkingCosts = [ $("#parking-cost-y-slider").slider("value"), $("#parking-cost-p-slider").slider("value") ];
        numCars = parseInt($("#num-cars").val());
        return new State(income, numBedrooms, numBedroomsRent, modes, commuteCosts, numWorkdays, parkingCosts, numCars, workAreaNames);
    }, Object.defineProperty(ՐՏ_4, "__doc__", {
        value: "Return a State instance containing the current values of the UI widgets.\nAll numerical fields are stored as integers."
    }), ՐՏ_4);
    function numToDollarStr(x, inverse) {
        inverse = inverse === void 0 ? false : inverse;
        var dollars;
        if (!inverse) {
            if (x === null || x === void 0) {
                return "n/a";
            }
            dollars = x.toFixed(0);
            dollars = dollars.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            return "$" + dollars;
        } else {
            if (x === "n/a") {
                return null;
            }
            return parseInt(x.replace("$", "").replace(",", ""));
        }
    }
    var getTable = (ՐՏ_5 = function getTable(feature) {
        var areaName, stats, commuteTime, total, fraction, percent, table;
        areaName = feature.properties.rental_area;
        stats = feature.properties.stats;
        if (stats.weeklyCommuteTime !== null) {
            commuteTime = stats.weeklyCommuteTime.toFixed(1) + "&nbsp;h";
        } else {
            commuteTime = "n/a";
        }
        if (stats.weeklyRent !== null && stats.weeklyCommuteCost !== null) {
            total = stats.weeklyTotalCost;
            fraction = stats.weeklyTotalCostFraction;
            percent = (fraction * 100).toFixed(1) + "%";
        } else {
            total = null;
            fraction = null;
            percent = "n/a";
        }
        table = "<h4>" + stats.areaName + "</h4>" + "<table>" + "<tr><td>Income per week</td><td>" + numToDollarStr(stats.weeklyIncome) + "</td>" + "<tr><td>Rent per week (" + stats.numBedroomsRent + " of " + stats.numBedrooms + " bd)</td><td>" + numToDollarStr(stats.weeklyRent) + "</td></tr>" + "<tr><td>Commute cost per week</td><td>" + numToDollarStr(stats.weeklyCommuteCost) + "</td></tr>" + "<tr><td>Commute time per week</td><td>" + commuteTime + "</td></tr>" + "<tr><td>Parking cost per week</td><td>" + numToDollarStr(stats.weeklyParkingCost) + "</td></tr>" + "<tr><td>Car cost per week</td><td>" + numToDollarStr(stats.weeklyCarOwnCost) + "</td></tr>" + "<tr><td>Total cost per week</td><td>" + numToDollarStr(total) + "</td></tr>" + "<tr><td>% of weekly income</td><td>" + percent + "</td></tr>" + "</table>";
        return table;
    }, Object.defineProperty(ՐՏ_5, "__doc__", {
        value: "Given an area unit feature with embedded stats of the form returned by\n``getAreaStats()``, format the stats in an HTML table, and\nreturn the result."
    }), ՐՏ_5);
    function rgbaToHex(s) {
        var ՐՏupk3, ՐՏitr9, ՐՏidx9;
        var a, result, x, h;
        ՐՏupk3 = [ s.slice(0, -1), s[s.length-1] ];
        s = ՐՏupk3[0];
        a = ՐՏupk3[1];
        result = "#";
        ՐՏitr9 = ՐՏ_Iterable(s);
        for (ՐՏidx9 = 0; ՐՏidx9 < ՐՏitr9.length; ՐՏidx9++) {
            x = ՐՏitr9[ՐՏidx9];
            h = Math.round(a * x + 255 * (1 - a)).toString(16);
            if (len(h) < 2) {
                h = "0" + h;
            }
            result += h;
        }
        return result;
    }
    function makeUI(lon, lat, maxBounds, markerLatLons, medianAnnualIncome, zoom, areas, areaData) {
        var ՐՏitr10, ՐՏidx10, ՐՏitr11, ՐՏidx11, ՐՏ_6, ՐՏ_7;
        var state, item, map, legend, info, workMarkers, k, title, symbol, url, customIcon, marker, m;
        state = new State(.84 * medianAnnualIncome, 3, 1, [ "bicycling", "bicycling" ], [ 0, 0 ], [ 5, 0 ], [ 0, 0 ], 0, null);
        $(function() {
            var sv, min, range, el;
            $("#income-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 100,
                "max": 2e5,
                "value": state.income,
                "step": 100,
                "slide": function(event, ui) {
                    $("#income").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    var state;
                    state = getState(getWorkAreaNames(workMarkers));
                    updateAreas(state);
                }
            });
            sv = $("#income-slider");
            $("#income").val(numToDollarStr(sv.slider("value")));
            min = sv.slider("option", "min");
            range = sv.slider("option", "max") - min;
            el = $("<label>&#9650;</label><br>").css("left", medianAnnualIncome / range * 100 + "%");
            $("#income-slider").append(el);
        });
        function adjustNumBedroomsRent() {
            var nb, group, nbr, x, item;
            nb = $("#num-bedrooms").val();
            group = $("#num-bedrooms-rent");
            nbr = group.val();
            if (nbr > nb) {
                nbr = nb;
                group.val(nb);
            }
            for (x = 1; x < 6; x++) {
                item = $("#num-bedrooms-rent li[value=" + x + "]");
                if (x === nbr) {
                    item.addClass("ui-selected");
                }
                if (x <= nb) {
                    item.removeClass("blocked");
                } else {
                    item.removeClass("ui-selected");
                    item.addClass("blocked");
                }
                group.selectable({
                    cancel: ".blocked"
                });
            }
        }
        $(function() {
            $("#num-bedrooms").selectable({
                "selected": function(event, ui) {
                    var state;
                    $("#num-bedrooms").val(ui.selected.value);
                    adjustNumBedroomsRent();
                    state = getState(getWorkAreaNames(workMarkers));
                    updateAreas(state);
                }
            });
        });
        item = $("#num-bedrooms li[value=" + state.numBedrooms + "]");
        item.addClass("ui-selected");
        $("#num-bedrooms").val(state.numBedrooms);
        adjustNumBedroomsRent();
        $(function() {
            $("#num-bedrooms-rent").selectable({
                "selected": function(event, ui) {
                    var state;
                    $("#num-bedrooms-rent").val(ui.selected.value);
                    state = getState(getWorkAreaNames(workMarkers));
                    updateAreas(state);
                }
            });
        });
        item = $("#num-bedrooms-rent li[value=" + state.numBedroomsRent + "]");
        item.addClass("ui-selected");
        $("#num-bedrooms-rent").val(state.numBedroomsRent);
        $(function() {
            $("#mode-y").selectable({
                "selected": function(event, ui) {
                    var mode, item, numWorkdays, state;
                    $("#mode-y").val(ui.selected.id);
                    mode = $("#mode-y").val();
                    if (mode !== "driving") {
                        $("#parking-cost-y").val("$0");
                        $("#parking-cost-y-slider").slider("value", 0);
                    } else {
                        item = $("#num-cars li.ui-selected");
                        if (item.val() === 0) {
                            item.removeClass("ui-selected");
                            $("#num-cars li:eq(1)").addClass("ui-selected");
                            $("#num-cars").val(1);
                        }
                    }
                    numWorkdays = parseInt($("#num-workdays-y").val());
                    if (numWorkdays) {
                        state = getState(getWorkAreaNames(workMarkers));
                        updateAreas(state);
                    }
                }
            });
        });
        item = $("#mode-y li[id=" + state.modes[0] + "]");
        item.addClass("ui-selected");
        $("#mode-y").val(state.modes[0]);
        $(function() {
            $("#mode-p").selectable({
                "selected": function(event, ui) {
                    var mode, item, numWorkdays, state;
                    $("#mode-p").val(ui.selected.id);
                    mode = $("#mode-p").val();
                    if (mode !== "driving") {
                        $("#parking-cost-p").val("$0");
                        $("#parking-cost-p-slider").slider("value", 0);
                    } else {
                        item = $("#num-cars li.ui-selected");
                        if (item.val() === 0) {
                            item.removeClass("ui-selected");
                            $("#num-cars li:eq(1)").addClass("ui-selected");
                            $("#num-cars").val(1);
                        }
                    }
                    numWorkdays = parseInt($("#num-workdays-p").val());
                    if (numWorkdays) {
                        state = getState(getWorkAreaNames(workMarkers));
                        updateAreas(state);
                    }
                }
            });
        });
        item = $("#mode-p li[id=" + state.modes[1] + "]");
        item.addClass("ui-selected");
        $("#mode-p").val(state.modes[1].id);
        $(function() {
            var s;
            $("#commute-cost-y-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 100,
                "value": state.commuteCosts[0],
                "step": 1,
                "slide": function(event, ui) {
                    $("#commute-cost-y").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    var numWorkdays, state;
                    numWorkdays = parseInt($("#num-workdays-y").val());
                    if (numWorkdays) {
                        state = getState(getWorkAreaNames(workMarkers));
                        updateAreas(state);
                    }
                }
            });
            s = $("#commute-cost-y-slider");
            $("#commute-cost-y").val(numToDollarStr(s.slider("value")));
        });
        $(function() {
            var s;
            $("#commute-cost-p-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 100,
                "value": state.commuteCosts[1],
                "step": 1,
                "slide": function(event, ui) {
                    $("#commute-cost-p").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    var numWorkdays, state;
                    numWorkdays = parseInt($("#num-workdays-p").val());
                    if (numWorkdays) {
                        state = getState(getWorkAreaNames(workMarkers));
                        updateAreas(state);
                    }
                }
            });
            s = $("#commute-cost-p-slider");
            $("#commute-cost-p").val(numToDollarStr(s.slider("value")));
        });
        $(function() {
            var s;
            $("#num-workdays-y-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 7,
                "value": state.numWorkdays[0],
                "step": 1,
                "slide": function(event, ui) {
                    $("#num-workdays-y").val(ui.value);
                },
                "stop": function(event, ui) {
                    var state;
                    state = getState(getWorkAreaNames(workMarkers));
                    updateAreas(state);
                }
            });
            s = $("#num-workdays-y-slider");
            $("#num-workdays-y").val(s.slider("value"));
        });
        $(function() {
            var s;
            $("#num-workdays-p-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 7,
                "value": state.numWorkdays[1],
                "step": 1,
                "slide": function(event, ui) {
                    $("#num-workdays-p").val(ui.value);
                },
                "stop": function(event, ui) {
                    var state;
                    state = getState(getWorkAreaNames(workMarkers));
                    updateAreas(state);
                }
            });
            s = $("#num-workdays-p-slider");
            $("#num-workdays-p").val(s.slider("value"));
        });
        $(function() {
            var s;
            $("#parking-cost-y-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 30,
                "value": state.parkingCosts[0],
                "step": 1,
                "slide": function(event, ui) {
                    $("#parking-cost-y").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    var numWorkdays, state;
                    numWorkdays = parseInt($("#num-workdays-y").val());
                    if (numWorkdays) {
                        state = getState(getWorkAreaNames(workMarkers));
                        updateAreas(state);
                    }
                }
            });
            s = $("#parking-cost-y-slider");
            $("#parking-cost-y").val(numToDollarStr(s.slider("value")));
        });
        $(function() {
            var s;
            $("#parking-cost-p-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 30,
                "value": state.parkingCosts[1],
                "step": 1,
                "slide": function(event, ui) {
                    $("#parking-cost-p").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    var numWorkdays, state;
                    numWorkdays = parseInt($("#num-workdays-p").val());
                    if (numWorkdays) {
                        state = getState(getWorkAreaNames(workMarkers));
                        updateAreas(state);
                    }
                }
            });
            s = $("#parking-cost-p-slider");
            $("#parking-cost-p").val(numToDollarStr(s.slider("value")));
        });
        $(function() {
            $("#num-cars").selectable({
                "selected": function(event, ui) {
                    var state;
                    $("#num-cars").val(ui.selected.value);
                    state = getState(getWorkAreaNames(workMarkers));
                    updateAreas(state);
                }
            });
        });
        item = $("#num-cars li[value=" + state.numCars + "]");
        item.addClass("ui-selected");
        $("#num-cars").val(state.numCars);
        map = L.map("map", {
            "center": [ lat, lon ],
            "zoom": zoom,
            "minZoom": 8,
            "maxZoom": 13,
            "maxBounds": maxBounds
        });
        map.scrollWheelZoom.disable();
        map.attributionControl.setPrefix("");
        legend = L.control({
            "position": "bottomleft"
        });
        legend.onAdd = function(map) {
            var div, content, n, i;
            div = L.DomUtil.create("div", "legend");
            content = "<h4>Cost as % of income</h4>";
            n = len(BINS);
            for (i = 0; i < n; i++) {
                content += '<span class="color" style="background:' + getColor(BINS[n - i - 1]) + '"></span><span>' + LABELS[n - i - 1] + "</span><br/>";
            }
            div.innerHTML = content;
            return div;
        };
        legend.addTo(map);
        L.control.scale({
            "imperial": false,
            "position": "topleft"
        }).addTo(map);
        info = L.control({
            position: "bottomright"
        });
        info.onAdd = function() {
            var div;
            div = L.DomUtil.create("div", "info");
            return div;
        };
        info.addTo(map);
        function updateInfo(feature) {
            feature = feature === void 0 ? null : feature;
            var table, div;
            if (feature !== null) {
                table = getTable(feature);
            } else {
                table = "<h4>Info box</h4>Hover over an area";
            }
            div = $(".info.leaflet-control").get(0);
            div.innerHTML = table;
        }
        updateInfo();
        workMarkers = [];
        for (k = 0; k < 2; k++) {
            if (k === 0) {
                title = "Your work";
                symbol = "y";
                url = "../images/work_marker_y.png";
            } else {
                title = "Your partner's work";
                symbol = "p";
                url = "../images/work_marker_p.png";
            }
            customIcon = L.icon({
                "iconUrl": url,
                "iconSize": [ 30, 70 ],
                "iconAnchor": [ 15, 35 ],
                "popupAnchor": [ 0, -35 ]
            });
            marker = L.marker(markerLatLons[k], {
                "draggable": true,
                "title": title,
                "icon": customIcon
            });
            workMarkers.append(marker);
        }
        ՐՏitr10 = ՐՏ_Iterable(workMarkers);
        for (ՐՏidx10 = 0; ՐՏidx10 < ՐՏitr10.length; ՐՏidx10++) {
            m = ՐՏitr10[ՐՏidx10];
            m.addTo(map);
        }
        ՐՏitr11 = ՐՏ_Iterable(workMarkers);
        for (ՐՏidx11 = 0; ՐՏidx11 < ՐՏitr11.length; ՐՏidx11++) {
            marker = ՐՏitr11[ՐՏidx11];
            marker.bindPopup("<h4>" + marker.options.title + "</h4>Undefined");
            marker.on("drag", function(e) {
                setWorkPopup(this);
            });
            marker.on("dragend", function(e) {
                var state;
                state = getState(getWorkAreaNames(workMarkers));
                updateAreas(state);
            });
        }
        var getAreaName = (ՐՏ_6 = function getAreaName(marker) {
            var latLon, layer, areaName;
            latLon = marker.getLatLng();
            try {
                layer = leafletPip.pointInLayer(latLon, areas, true)[0];
            } catch (ՐՏ_Exception) {
                return null;
            }
            if (layer) {
                areaName = layer.feature.properties.rental_area;
            } else {
                areaName = null;
            }
            return areaName;
        }, Object.defineProperty(ՐՏ_6, "__doc__", {
            value: "Return the name of the area that the given marker lies in."
        }), ՐՏ_6);
        function getWorkAreaNames(workMarkers) {
            workMarkers = workMarkers === void 0 ? null : workMarkers;
            var m, result;
            if (workMarkers !== null) {
                result = (function() {
                    var ՐՏidx12, ՐՏitr12 = ՐՏ_Iterable(workMarkers), ՐՏres = [], m;
                    for (ՐՏidx12 = 0; ՐՏidx12 < ՐՏitr12.length; ՐՏidx12++) {
                        m = ՐՏitr12[ՐՏidx12];
                        ՐՏres.push(getAreaName(m));
                    }
                    return ՐՏres;
                })();
            } else {
                result = null;
            }
            return result;
        }
        var setWorkPopup = (ՐՏ_7 = function setWorkPopup(marker) {
            var areaName, text;
            areaName = getAreaName(marker);
            text = "<h4>" + marker.options.title + "</h4>";
            if (areaName) {
                text += areaName;
            } else {
                text += "Undefined";
            }
            marker.setPopupContent(text);
            marker.openPopup();
        }, Object.defineProperty(ՐՏ_7, "__doc__", {
            value: "Set the content of the given marker's popup,undefined\nand open the popup."
        }), ՐՏ_7);
        function getColor(x) {
            if (x === null) {
                return GREY;
            } else {
                return COLOR_SCALE(x);
            }
        }
        function areaStyle(feature) {
            var c;
            c = getColor(feature.properties.stats.weeklyTotalCostFraction);
            return {
                "fillColor": c,
                "fillOpacity": 1,
                "color": "black",
                "weight": .5,
                "opacity": 1
            };
        }
        function highlightFeature(e) {
            var layer;
            layer = e.target;
            layer.setStyle({
                "weight": 2
            });
            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
            }
            updateInfo(layer.feature);
        }
        function resetHighlight(e) {
            var layer;
            layer = e.target;
            layer.setStyle({
                "weight": .5
            });
            layer._map.closePopup();
            updateInfo();
        }
        function zoomToFeature(e) {
            map.fitBounds(e.target.getBounds());
        }
        function onEachFeature(feature, layer) {
            layer.on({
                "mouseout": resetHighlight,
                "click": zoomToFeature,
                "mouseover": highlightFeature
            });
        }
        areas = L.geoJson(areas, {
            "onEachFeature": onEachFeature
        }).addTo(map);
        function updateAreas(state) {
            areas.eachLayer(function(layer) {
                var areaName, stats;
                areaName = layer.feature.properties.rental_area;
                stats = areaData.getAreaStats(state, areaName);
                layer.feature.properties.stats = stats;
                layer.setStyle(areaStyle(layer.feature));
            });
        }
        updateAreas(state);
    }
    function main() {
        var data, lon, lat, maxBounds, markerLatLons, medianAnnualIncome, zoom, spinner;
        data = $.parseJSON($("#data").html());
        lon = data["lon"];
        lat = data["lat"];
        maxBounds = data["maxBounds"];
        markerLatLons = data["markerLatLons"];
        medianAnnualIncome = data["medianAnnualIncome"];
        zoom = data["zoom"];
        spinner = new Spinner().spin($("#map").get(0));
        $.when($.getJSON(data["areasFile"]), $.getJSON(data["rentsFile"]), $.getJSON(data["commuteCostsFile"])).done(function(a, b, c) {
            var areas, areaData;
            areas = a[0];
            areaData = new AreaData(b[0], c[0]["index_by_name"], c[0]["matrix"]);
            spinner.stop();
            makeUI(lon, lat, maxBounds, markerLatLons, medianAnnualIncome, zoom, areas, areaData);
        });
    }
    main();
})();
var ՐՏ_8;
})();
