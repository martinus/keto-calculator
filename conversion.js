// global variable that is set to true when google is loaded
var google_is_loaded_bool = false;
var weight_table = [];
var last_weight_table_input = [];
var maintainence_fat_protein_carbs = [];

var calc_deadline = 0;
// delay in milliseconds
var execution_delay = 500;

// from http://www.bodyrecomposition.com/fat-loss/setting-the-deficit-small-moderate-or-large.html
var deficit_levels = [
	[-1e9, "#e61717", "You will gain weight"], // minus to 0
	[0, "#1717e6", "Zero deficit: You will maintain your current weight."], // 0-1%
	[1, "#177ee6", "Very little deficit, choose a higher deficit to lose faster."], // 1-10-% 
	[10, "#17e6e6",  "Small deficit: Best for athletes who are already lean."], // 10-15%
	[15, "#17e67e",  "Average deficit. This should be easily sustainable, good choice for a start."], // 15-20%
	[20, "#17e617",  "Moderate Deficit: Fast weight loss with moderate difficulty."], // 20-25
	[25, "#7ee617",  "Large Deficit: This is hard, give it a try for two weeks."], // 25-30
	[30, "#e6e617",  "That's a huge deficit. Try a 20% deficit if you fail."], // 35-
	[35, "#e67e17",  "Severe Deficit: Are you sure? Try a 20% deficit if you fail"], // 30-35%
	[45, "#e61717",  "That is an enormous deficit and extremely hard. Start with 20% if you are unsure."] // 40%
];


function toggle_visibility(id, elem) {
	var e = document.getElementById(id);
	if(e.style.display == 'block') {
		e.style.display = 'none';
		elem.className = elem.className.replace(" expandeble_expanded", "");
	} else {
		e.style.display = 'block';
		elem.className += " expandeble_expanded";
	}
}

// from http://stackoverflow.com/questions/4060004/calculate-age-in-javascript
function calcAge(dateString) {
  var birthday = +new Date(dateString);
  // 24 * 3600 * 365.242 * 1000
  return (Date.now() - birthday) / 31556908800.0;
}

// try to nicely round number
function abbrNum(n, decPlaces) {
	if (n == 0) {
		return n;
	}
	decPlaces -= Math.floor(Math.log(Math.abs(n)) / Math.log(10)) + 1;
	var f = Math.pow(10, decPlaces);
	return Math.round(n * f) / f;
}

function set_cookie(form, ignore_list) {
	// set cookie with the active field
	var expires = new Date();
	expires.setTime(expires.getTime() + 365*24*60*60*1000);
	expires = ";expires=" + expires.toGMTString();
	
	// build cookie from all form data
	for (var i=0; i<form.length; ++i) {
		var e = form[i];
		if (!e.disabled
			&& (("text" == e.type && "" != e.value) || ("radio" == e.type && e.checked)))
		{
			var j = 0
			while (j != ignore_list.length && ignore_list[j] != e.name) {
				++j
			}
			if (j == ignore_list.length) {
				document.cookie = e.name + "=" + escape(e.value) + expires;
			}
		}
	}
}


function radio_val(r) {
	for (var i=0; i<r.length; i++) {
		if (r[i].checked) {
			return r[i].value;
		}
	}
	return false;
}


function update_by_name(name, val) {
	var elems = document.getElementsByClassName(name);
	for (var i=0; i<elems.length; ++i) {
		elems[i].innerHTML = val;
	}
}

function update_by_id(name, val) {
	var elem = document.getElementById(name);
	elem.innerHTML = val;
}

// about 7.7 kcal of bodyfat tissue is actually fat.
// see http://www.caloriesperhour.com/tutorial_pound.php
// based on this conversation http://www.reddit.com/r/keto/comments/12amhq/keto_calculator_20/c6ux0xt?context=3
//
// Since when you lose fat your bmr changes, for accurate numbers I recalculate each day.
function calc_expected_loss_kg(days, max_kcal_per_lb_per_day, bodyfat_percent, essential_bodyfat_kg, target_kcal, kg, height, age, sex, bmr_fact) {
	// creates a data table that can be used for google charts.	
	//update_by_id("debug", days+" "+max_kcal_per_lb_per_day+" "+ bodyfat_percent+" "+ essential_bodyfat_kg+" "+ target_kcal+" "+ kg+" "+ height+" "+ age+" "+ sex+" "+ bmr_fact);	

	var table = [];
		
	var my_kg = kg;
	var lean_mass = kg * (100 - bodyfat_percent) / 100.0;
	
	var kcal_min;
	var day = 0;
	for (day=0; day<days; ++day) {
		var bmr = 9.99 * my_kg + 6.25 * height - 4.92 * (age+day/365.242) + sex;
		var expenditure = bmr * bmr_fact;
		
		// when kcal_min is too high (not enough energy can be provided by bodyfat), expect we eat kcal_min.
		var bodyfat_kg = my_kg - lean_mass;
		
		// given the daily expenditure, find out how much kcal you have to eat because that can not come from bodyfat
		// max_kcal_per_lb_per_day kcal/lb is max_kcal_per_lb_per_day/0.45359237 kcal/kg
        // don't allwo the loss of essential bodyfat.
		kcal_min = expenditure - max_kcal_per_lb_per_day/0.45359237 * bodyfat_kg;
		
		var expected_loss_kg = (target_kcal - expenditure) / (7.7 * 1000);
				
		if (kcal_min > target_kcal) {
			expected_loss_kg = (kcal_min - expenditure) / (7.7 * 1000);
		}		
				
		if (bodyfat_kg <= essential_bodyfat_kg) {
			expected_loss_kg = 0;
		}		
		
		// TODO do something with kcal_min!
		table.push([my_kg, bodyfat_kg, kcal_min, target_kcal, expected_loss_kg]);

		my_kg += expected_loss_kg;
	}
	return [my_kg - kg, table];
}

function mark_empty_fields(d) {
	// check data of form elements
	for (var i=0; i<d.elements.length; ++i) {
		var el = d.elements[i];
		if (el.type == "text" && !el.disabled) {
			if (isNaN(parseFloat(el.value))) {
				el.style.outline = "2px solid #99cc00";
			} else {
				el.style.outline = "";
			}
		}
	}	
	
	// check if radio's are selected
	var is_selected = {}
	for (var i=0; i<d.elements.length; ++i) {
		var el = d.elements[i];
		if (el.type == "radio" && el.checked) {
			is_selected[el.name] = true;
		}
	}
	
	// now that we know all radio's that are selected, highlight the non-selected ones
	for (var i=0; i<d.elements.length; ++i) {
		var el = d.elements[i];
		if (el.type == "radio") {
			if (is_selected[el.name]) {
				el.style.outline = "";
			} else {
				el.style.outline = "2px solid #99cc00";
			}
		}
	}	
}	

function check_adblocker() {
	var ad = document.getElementById("firstad");
	var is_hidden = ad.clientHeight == 0;
	if (is_hidden) {
		document.getElementById("ads_disabled").style.display = 'block';
	} else {
		// ad is visible! Hide text view.
		document.getElementById("ads_disabled").style.display = 'none';
	}
}


function wait_until_deadline(e) {
	var current_time = (new Date()).getTime();
	if (current_time < calc_deadline) {
		//update_by_id("debug", current_time + " timeout");	
		setTimeout(function(){ wait_until_deadline(e) }, calc_deadline - current_time);
	} else {
		// waited enough! perform the update.
		//update_by_id("debug", current_time + " EXECUTING!");	
		calc_deadline = 0;
		
		// draw time consuming stuff now
		draw_pies(maintainence_fat_protein_carbs);
		draw_chart(weight_table);	
	}
}

function calc_handler(e) {
	// perform fast updates right now
	update_calculations(e);

	// set a deadine
	var current_time = (new Date()).getTime();
	
	if (calc_deadline == 0) {
		// start a new delayed execution
		calc_deadline = current_time + execution_delay;
		setTimeout(function(){ wait_until_deadline(e) }, calc_deadline - current_time);
	} else {
		// we have an execution waiting, just update the deadline but don't start another one
		calc_deadline = current_time + execution_delay;
	}
}

function update_calculations(e) {
	// Also see this discussion: http://www.reddit.com/r/keto/comments/12amhq/keto_calculator_20/c6vq31e?context=3
	// and this: http://www.reddit.com/r/keto/comments/12amhq/keto_calculator_20/c6vvu7f?context=3
	// and finally, since essential fat was added, this: http://www.reddit.com/r/keto/comments/1e6czr/essential_body_fat_support_in_keto_calculator/c9x82qo
	
	// 290 kJ/kg d
	// 1 kJ = 0.239005736 kcal
	// 1 kg = 0.453592 pound
	// is about 31.4
	var max_kcal_per_lb_per_day = 290 * 0.239005736 * 0.453592;
	

	var d = document.data;
	
	// e is null when called from cookie
	if (e) {
		// lbs/kg conversion
		if (e.target == d.lbs) {
			// update kg
			var lbs = parseFloat(d.lbs.value);
			if (!isNaN(lbs)) {
				d.kg.value = abbrNum(lbs * 0.45359237, 3);
			} else {
				d.kg.value = "";
			}
		} else if (e.target == d.kg) {
			var kg = parseFloat(d.kg.value);
			if (!isNaN(kg)) {
				d.lbs.value = abbrNum(kg / 0.45359237, 3);
			} else {
				d.lbs.value = "";
			}
		}
		
		// cm/ feet+inch conversion
		if (e.target == d.height) {
			var cm = parseFloat(d.height.value);
			if (!isNaN(cm)) {
				var feet = Math.floor(0.032808399 * cm);
				var inch = Math.round((cm - (feet / 0.032808399)) / 2.54);
				d.feet.value = feet;
				d.inch.value = inch
			} else {
			}
		} else if (e.target == d.feet || e.target == d.inch) {
			var feet = parseFloat(d.feet.value);
			var inch = parseFloat(d.inch.value);
			if (!isNaN(feet) && !isNaN(inch)) {
				var cm = feet / 0.032808399 + inch * 2.54;
				d.height.value = Math.round(cm);
			} else {
				d.height.value = "";
			}
		}
	}

	var bday = d.bday.value;
	var age = NaN
	if (bday != "") {
		age = calcAge(bday);
		var years = Math.floor(age);
		var months = Math.floor((age - Math.floor(age)) * 12);
		update_by_name("years", years);
		update_by_name("months", months);
		
		if (isNaN(age) || age > 100 || age < 5) {
            update_by_id("date_warning", "WARNING: Could not process date! use MM/DD/YYYY, e.g. 8/20/1979");
		} else {
			update_by_id("date_warning", "");
		}
	}
	
	//var age = parseFloat(d.age.value);

	
	var is_female = NaN
	var sex = NaN
	var kg = parseFloat(d.kg.value);
	var height = parseFloat(d.height.value);
	var estimated_bodyfat_percent = NaN;
	
	if (!isNaN(radio_val(d.sex))
		&& !isNaN(kg)
		&& !isNaN(height)
		&& !isNaN(age))
	{
        is_female = parseInt(radio_val(d.sex), 10) == 1;
        if (is_female) {
            sex = -161;
        } else {
            sex = 5;
        }
        
		var bmr = 9.99 * kg + 6.25 * height - 4.92 * age + sex;
		d.bmr.value = Math.round(bmr);
		
		// estimate body fat percentage, based on http://ajcn.nutrition.org/content/83/2/252.full.pdf
		var bf;
		if (is_female) {
			bf = 1.181 * kg / (height/100.0) - 24.18;
		} else {
			bf = 1.120 * kg / (height/100.0) - 30.84;
		}
		estimated_bodyfat_percent = Math.round(100 * bf / kg);
		update_by_name("estimated_bodyfat_percent", estimated_bodyfat_percent);
	} else {
		d.bmr.value = "";
	}
	
	// calculate daily energy expenditure
	update_by_name("expenditure_kcal", "");
	var level = parseFloat(radio_val(d.level));
	var expenditure = NaN;
	var bmr_fact = NaN;
	if (!isNaN(is_female)
        && !isNaN(level)
		&& !isNaN(bmr))
	{
		// factors are based on http://en.wikipedia.org/wiki/Harris-Benedict_equation
		// it scales from 1.2 to 1.9 in 4 steps (5 levels)
		var min_fact = 1.2;
		var max_fact = 1.9;
		bmr_fact = min_fact + level * (max_fact - min_fact)/4;
		expenditure = bmr * bmr_fact;
		d.energy.value = Math.round(expenditure);
		update_by_name("expenditure_kcal", Math.floor(expenditure));
		d.kcal_max_form.value = Math.floor(expenditure);
	} else {
		d.energy.value = "";
		d.kcal_max_form.value = "";
	}
	
	
	// calculate daily protein
	update_by_name("protein_recommendation_g", "");	
	update_by_name("min_protein_g_per_kg", "");
	update_by_name("max_protein_g_per_kg", "");	
	update_by_name("min_protein_g_per_lb", "");
	update_by_name("max_protein_g_per_lb", "");
	
	var bodyfat = parseFloat(d.bodyfat.value);
    var essential_bodyfat_kg = 0;
	if (!isNaN(bodyfat)
		&& !isNaN(kg))
	{
		// The min protein levels are based on 
		// http://www.bodyrecomposition.com/fat-loss/protein-intake-while-dieting-qa.html
		// and the book
		// "The Art and Science of Low Carbohydrate Performance".
		// 
		// max protein level is based on this
		// http://bayesianbodybuilding.com/the-myth-of-1glb-optimal-protein-intake-for-bodybuilders/	
		//
		// units are gram per kg lean bodymass
		var min_protein_g_per_kg = 0.6/0.45359237;
		var max_protein_g_per_kg = 1.0/0.45359237;
		
		var lean_bodymass = (kg * (1 - bodyfat/100));

        // calculate the essential bodyfat in kg.
        // Use 3% for men, and 11% for women.
        var essential_fact = 0.03;
        if (is_female) {
            essential_fact = 0.11;
        }
        essential_bodyfat_kg = lean_bodymass * (essential_fact / (1 - essential_fact));
        
		var min_protein = Math.ceil(min_protein_g_per_kg * lean_bodymass);
		var max_protein = Math.floor(max_protein_g_per_kg * lean_bodymass);
		d.protein_min.value = min_protein;
		d.protein_max.value = max_protein;
		
		// calc protein recommendation
		var protein_recommendation_fact = (min_protein_g_per_kg + level * (max_protein_g_per_kg - min_protein_g_per_kg)/4);
        
        // make sure the recommendation is between the min and max
		var protein_recommendation_g = Math.round(lean_bodymass * protein_recommendation_fact);
        protein_recommendation_g = Math.max(protein_recommendation_g, min_protein);
        protein_recommendation_g = Math.min(protein_recommendation_g, max_protein);
		update_by_name("protein_recommendation_g", protein_recommendation_g);
		
		update_by_name("min_protein_g", min_protein);
		update_by_name("max_protein_g", max_protein);
		update_by_name("min_protein_g_per_kg", abbrNum(min_protein_g_per_kg, 2));
		update_by_name("max_protein_g_per_kg", abbrNum(max_protein_g_per_kg, 2));
		
		update_by_name("min_protein_g_per_lb", abbrNum(min_protein_g_per_kg*0.45359237, 2));
		update_by_name("max_protein_g_per_lb", abbrNum(max_protein_g_per_kg*0.45359237, 2));
		
		update_by_name("bodyfat_percentage", bodyfat);
		update_by_name("lean_kg", Math.round(lean_bodymass));
		update_by_name("lean_lbs", Math.round(lean_bodymass/0.45359237));
		
		var fat_kg = kg * bodyfat/100;
		update_by_name("fat_kg", Math.round(fat_kg));
		update_by_name("fat_lbs", Math.round(fat_kg/0.45359237));
        
        update_by_name("essential_fat_kg", abbrNum(essential_bodyfat_kg, 2));
        update_by_name("essential_fat_lbs", abbrNum(essential_bodyfat_kg/0.45359237, 2));
        
        if (essential_bodyfat_kg >= fat_kg) {
            update_by_id("bodyfat_percentage_warning", "WARNING: Your body fat percentage is too low!");
        } else {
            update_by_id("bodyfat_percentage_warning", "");
        }
	} 

	// read in chosen protein
	var protein_g = parseFloat(d.protein_chosen.value);
	update_by_name("protein", protein_g);
	
	update_by_id("protein_warning", "");
	update_by_name("chosen_protein_g_per_kg", "");
	update_by_name("chosen_protein_g_per_lb", "");
	
	if (!isNaN(protein_g)
		&& !isNaN(kg)
		&& !isNaN(bodyfat))
	{
		var chosen_g_per_kg = protein_g / (kg * (1 - bodyfat/100));
		update_by_name("chosen_protein_g_per_kg", abbrNum(chosen_g_per_kg, 2));
		update_by_name("chosen_protein_g_per_lb", abbrNum(chosen_g_per_kg*0.45359237, 2));
		if (parseFloat(d.protein_min.value) > protein_g) {
			update_by_id("protein_warning", "WARNING: protein too low!");
		} else if (parseFloat(d.protein_max.value) < protein_g) {
			/*
			var url = "http://preview.images.memegenerator.net/Instance/Preview?imageID=203665&generatorTypeID=&panels=&text0=";
			url += protein_g;
			url += "g%20protein&text1=is%20too%20damn%20high&text2=&text3=";
			*/
			var url = "proteintoohigh_small.jpg";
			
			// easter egg! ;)
			update_by_id("protein_warning", "WARNING: protein too high!<br /><img width=\"190\" height=\"227\" src=" + url + " />");
			// http://preview.images.memegenerator.net/Instance/Preview?imageID=203665&generatorTypeID=&panels=&text0=132g%20protein&text1=is%20too%20damn%20high&text2=&text3=
		} 
	}
	
	//	read in carbs
	var carbs_g = parseFloat(d.carbs.value);
	update_by_name("carbs", Math.round(carbs_g));
	update_by_name("kcal_min", "");	
	
	// calculate minimum caloric intake based on fixed calories, proteins, and maximum rate of fat loss.	
	var kcal_min = NaN
	var fat_g_min = NaN
	if (!isNaN(bmr)
		&& !isNaN(carbs_g)
		&& !isNaN(protein_g)
		&& !isNaN(expenditure))
	{
		// calculate total loseable bodyfat weight in kg
		var bodyfat_kg = bodyfat * kg / 100.0 - essential_bodyfat_kg;

		// given the daily expenditure, find out how much kcal you have to eat because that can not come from bodyfat
		// max_kcal_per_lb_per_day kcal/lb is max_kcal_per_lb_per_day/0.45359237 kcal/kg
		kcal_min = expenditure - max_kcal_per_lb_per_day/0.45359237 * bodyfat_kg;
		
		// make sure kcal_min is not below required carb+protein intake.
		// also make sure to have at least 30g of fat to prevent formation of gallstones (see the art and science of low carbohydrate living, page 168)
		var kcal_nonfat = 4*carbs_g + 4*protein_g;
		kcal_min = Math.max(kcal_nonfat + 30*9, kcal_min);
		var kcal_fat = expenditure - kcal_nonfat;
		
		// while we are at it, calculate fat_g_min.
		fat_g_min = Math.ceil((kcal_min - kcal_nonfat)/9.0);		
		
		// fat_g_min might be below 0 because carbs + protein is already large enough for the min intake.
		// Just set it to 0, because you can't eat negative fat...
		d.fat_min_form.value = fat_g_min;
		update_by_name("kcal_min", Math.ceil(kcal_min));
		d.kcal_min_form.value = Math.ceil(kcal_min);
		update_by_name("fat_g_min", fat_g_min);
		update_by_name("kcal_nonfat", Math.round(kcal_nonfat));
		update_by_name("kcal_fat", Math.round(kcal_fat));
	}
	
	if (!isNaN(kcal_min)
		&& !isNaN(expenditure))
	{
		var min_deficit_percent = 100 * (expenditure - kcal_min) / expenditure;
		d.min_deficit_percent_form.value = Math.floor(min_deficit_percent);
	}	
	
	//	read in target fat g
	var target_fat_g = NaN;
	var target_kcal = NaN;
	var target_deficit = NaN;
	if (!isNaN(carbs_g)
		&& !isNaN(protein_g))
	{
		if (e && e.target == d.target_fat_form) {
			// read fat and update target_kcal
			target_fat_g = parseFloat(d.target_fat_form.value);
			target_kcal = carbs_g*4 + protein_g*4 + target_fat_g*9;
			target_deficit = 100 * (expenditure - target_kcal) / expenditure;
			if (!isNaN(target_kcal)) {
				d.target_kcal_form.value = Math.round(target_kcal);
				d.target_deficit_form.value = Math.round(target_deficit);
			} else {
				d.target_kcal_form.value = "";
				d.target_deficit_form.value = "";
			}
		} else  if (e && e.target == d.target_deficit_form) {
			// read target_deficit_form and update the rest
			target_deficit = parseFloat(d.target_deficit_form.value);
			target_kcal = expenditure * (1 - target_deficit/100);
			target_fat_g = Math.max(0, (target_kcal - carbs_g*4 - protein_g*4)/9);
			if (!isNaN(target_deficit)) {
				d.target_fat_form.value = Math.round(target_fat_g);
				d.target_kcal_form.value = Math.round(target_kcal);
			} else {
				d.target_fat_form.value = "";
				d.target_kcal_form.value = "";
			}			
		} else {
			// use kcal as the last one, this is also the most precise one.
			// read target_kcal and update target_fat_g
			target_kcal = parseFloat(d.target_kcal_form.value);
			target_fat_g = Math.max(0, (target_kcal - carbs_g*4 - protein_g*4)/9);
			target_deficit = 100 * (expenditure - target_kcal) / expenditure;
			if (!isNaN(target_fat_g)) {
				d.target_fat_form.value = Math.round(target_fat_g);
				d.target_deficit_form.value = Math.round(target_deficit);
			} else {
				d.target_fat_form.value = "";
				d.target_deficit_form.value = "";
			}
		}
	}	
	
	if (!isNaN(target_fat_g)
		&& !isNaN(target_kcal)
		&& !isNaN(carbs_g)
		&& !isNaN(protein_g)
		&& !isNaN(kcal_min)
		&& !isNaN(expenditure))
	{	
		
		update_by_name("target_kcal", "");
		update_by_name("chosen_loss_kg", "");
		update_by_name("chosen_loss_lbs", "");
		update_by_name("max_loss_kg", "");
		update_by_name("max_loss_lbs", "");
		

		update_by_name("target_kcal", Math.round(target_kcal));
		update_by_name("deficit_kcal", Math.floor(expenditure) - Math.round(target_kcal));
				
		// show warning
		if (target_kcal < kcal_min) {
			update_by_id("kcal_warning", "WARNING: Too low! You will lose muscles.");			
			var elem = document.getElementById("kcal_warning");
			elem.style.textShadow = "red 0.1em 0.1em 1em";
		} else {
			var td = Math.round(target_deficit);
			// search target deficit
			var i=deficit_levels.length - 1;
			while (i != 0 && deficit_levels[i][0] > td) {
				--i;
			}
			update_by_id("kcal_warning", deficit_levels[i][2]);
			var elem = document.getElementById("kcal_warning");
			elem.style.color = "black";
			elem.style.textShadow = deficit_levels[i][1] + "  0.1em 0.1em 1em";
		}
		
		var data = calc_expected_loss_kg(365, max_kcal_per_lb_per_day, bodyfat, essential_bodyfat_kg, target_kcal, kg, height, age, sex, bmr_fact);
		var current_weight_table_input = [bodyfat, target_kcal, kg, height, age, sex, bmr_fact];
		weight_table = [data[1], current_weight_table_input];
				
		data = calc_expected_loss_kg(30, max_kcal_per_lb_per_day, bodyfat, essential_bodyfat_kg, target_kcal, kg, height, age, sex, bmr_fact);
		var expected_loss_kg = data[0];
		
		update_by_name("chosen_loss_kg", abbrNum(-expected_loss_kg, 2));
		update_by_name("chosen_loss_lbs", abbrNum(-expected_loss_kg/0.45359237, 2));
		
		var max_loss_kg = calc_expected_loss_kg(30, max_kcal_per_lb_per_day, bodyfat, essential_bodyfat_kg, kcal_min, kg, height, age, sex, bmr_fact)[0];
		update_by_name("max_loss_kg", abbrNum(max_loss_kg, 2));
		update_by_name("max_loss_lbs", abbrNum(max_loss_kg/0.45359237, 2));		
	}
	
	// calculate fat_g based on target kcal
	var fat_g = NaN;
	if (!isNaN(target_kcal)
		&& !isNaN(carbs_g)
		&& !isNaN(protein_g))
	{
		fat_g = (target_kcal - 4*carbs_g - 4*protein_g)/9;
		fat_g = Math.max(0, fat_g);
		// TODO warn when below!
		update_by_name("fat", Math.round(fat_g));
	}
	
	
	// calculate max fat intake	
	var fat_g_max = NaN;
	update_by_name("fat_g_max", "");
	
	if (!isNaN(carbs_g)
		&& !isNaN(protein_g)
		&& !isNaN(expenditure))
	{
		fat_g_max = (expenditure - 4*protein_g - 4*carbs_g) / 9;
		update_by_name("fat_g_max", Math.floor(fat_g_max));
		d.fat_max_form.value = Math.floor(fat_g_max);
	} 
	
	// calculate percentage based on kcal
	if (!isNaN(fat_g)
		&& !isNaN(carbs_g)
		&& !isNaN(protein_g)
		&& !isNaN(expenditure)
		&& !isNaN(target_kcal))
	{
		var carbs_proc = Math.round(carbs_g*4 / target_kcal * 100);
		var protein_proc = Math.round(protein_g*4 / target_kcal * 100);
		var fat_proc = 100 - carbs_proc - protein_proc;
		
		var carbs_cal = Math.round(carbs_g*4);
		var protein_cal = Math.round(protein_g*4);
		var fat_cal = Math.round(target_kcal) - protein_cal - carbs_cal;
		maintainence_fat_protein_carbs = [expenditure, fat_cal, protein_cal, carbs_cal];
		
		if (carbs_proc > 100 || carbs_proc < 0 || protein_proc > 100 || protein_proc < 0) {
			update_by_name("carbs_proc", "-");
			update_by_name("protein_proc", "-");
			update_by_name("fat_proc", "-");
			
			update_by_name("carbs_kcal", "-");
			update_by_name("protein_kcal", "-");
			update_by_name("fat_kcal", "-");
		} else {
			update_by_name("carbs_proc", carbs_proc);
			update_by_name("protein_proc", protein_proc);
			update_by_name("fat_proc", fat_proc);
			
			update_by_name("carbs_kcal", carbs_cal);
			update_by_name("protein_kcal", protein_cal);
			update_by_name("fat_kcal", fat_cal);
		}
	}
	
	
	// write summary
	if (isNaN(fat_g)) {
		update_by_name("fat", "-")
	}
	if (isNaN(protein_g)) {
		update_by_name("protein", "-")
	}
	if (isNaN(carbs_g)) {
		update_by_name("carbs", "-")
	}
	
	
	// generate reddit_post_str
	var version = document.getElementById("version_number").innerHTML;
    // remove leading and trailing whitespace
    version = version.replace(/^\s+|\s+$/g, '');
	
	var nl = "\n"
	
	var str = "Replace this line with your question\n"
	str += "\n---" + nl
	str += "*Generated by [Keto Calculator](http://keto-calculator.ankerl.com) " + version + "*" + nl + nl;
	str += Math.floor(age) + "/";
	if (is_female) {
		str += "F";
	} else {
		str += "M";
	}
	str += "/" + d.feet.value + "'" + d.inch.value + "\" | ";
	str += "CW " + d.lbs.value + " | "
	str += d.bodyfat.value + "% BF | ";
	
	var level_to_shorttext = {
		0: "Mostly sedentary",
		1: "Lightly active",
		2: "Moderately active",
		3: "Very active",
		4: "Extremely active"
	}
	str += level_to_shorttext[level] + nl + nl;
	
	str += "* " + Math.round(target_kcal) + " kcal Goal, a " + Math.round(target_deficit) + "% deficit. (" + Math.round(kcal_min) + " min, " + Math.round(expenditure) + " max)"+ nl;
	str += "* " + carbs_g + "g Carbohydrates" + nl;
	str += "* " + protein_g + "g Protein (" + d.protein_min.value + "g min, " + d.protein_max.value + "g max)" + nl;
	str += "* " + Math.round(fat_g) + "g Fat (" + fat_g_min + "g min, " + Math.floor(fat_g_max) + "g max)" + nl;
	str += nl;
	str += "----" + nl;
	
	d.reddit_copypaste.value = str;
	
	// build url
	url = "http://www.reddit.com/r/keto/submit?"
	url += "text=" + encodeURIComponent("\n\n" + str);
	
	update_by_name("redditsubmit", "<a href="+url+" target=\"_blank\">Create a /r/keto post</a>");
	
	mark_empty_fields(d);
	
	
	// set cookie before chart, in case when something goes wrong
	set_cookie(d, ["target_fat_form"]);
}

function ary(e) {
	var a = [];
	for (var i=0; i<e.length; ++i) {
		a.push(e[i]);
	}
	return a;
}

function load_cookie() {
	// load data from cookie, if present
	if (document.cookie) {
		var fields = document.cookie.split("; ");
		
		for (var i=0; i<fields.length; ++i) {
			var idx = fields[i].indexOf("=");
			var key = fields[i].substr(0, idx);
			var val = unescape(fields[i].substr(idx+1));
			
			var elem = document.data.elements[key];
			if (elem) {
				if ("text" == elem.type) {
					elem.value = val;
				} else {
					for (var j=0; j<elem.length; ++j) {
						if ("radio" == elem[j].type && elem[j].defaultValue == val) {
							elem[j].checked = true;
						}
					}
				}
			}
		}
		
		// disable chart drawing
		//document.data.chart_weight_type[0].checked = false
		//document.data.chart_weight_type[1].checked = false
		
		// initiate recalculation
		calc_handler(null);
	}
}

function google_is_loaded() {
	google_is_loaded_bool = true;
	draw_pies(maintainence_fat_protein_carbs);
	draw_chart(weight_table);
}

function is_similar(a, b, closeness) {
	if (a.length != b.length) {
		return false;
	}
	for (var i=0; i<a.length; ++i) {
		if (Math.abs(a[i] - b[i])/a[i] > closeness) {
			return false;
		}
	}
	
	return true;
}

function draw_pies(maintainence_fat_protein_carbs) {
	if (maintainence_fat_protein_carbs.length != 4 || !google_is_loaded_bool) {
		return;
	}
	
	var expenditure = Math.floor(maintainence_fat_protein_carbs[0]);
	var fat = Math.round(maintainence_fat_protein_carbs[1]);
	var protein = Math.round(maintainence_fat_protein_carbs[2]);
	var carbs = Math.round(maintainence_fat_protein_carbs[3]);
	
	// draw full maintainence chart
	var data_m = new google.visualization.DataTable();
	data_m.addColumn('string', 'Ratio');
	data_m.addColumn('number', 'Calories');
	data_m.addRow(['Maintainence Calories', expenditure]);
	
	var options_m = { 
		'chartArea': {
			'width':176,
			'height':176
		},
		'width':200,
		'height':200,
		'colors':['#A3A3A3'],
		'legend':'none',
		'fontSize':10,
		'pieSliceText':'value'
	};
	
	var chart_m = new google.visualization.PieChart(document.getElementById('pie_maintainence'));
	chart_m.draw(data_m, options_m);	

	// draw actual chart
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Ratio');
	data.addColumn('number', 'Calories');
	data.addRows([
		['Fat', Math.round(fat)],
		['Protein', protein],
		['Carbohydrate', carbs]
	]);
	
	var area_ratio = Math.sqrt(fat+protein+carbs) / Math.sqrt(expenditure);
	var options = {
		'chartArea': {
			'width':176*area_ratio,
			'height':176*area_ratio
		},
		'width':176*area_ratio + 24,
		'height':176*area_ratio + 24,
		'colors':['#264A73','#709500','#E60144'],
		'legend':'none',
		'fontSize':10
	};
		
	var chart = new google.visualization.PieChart(
		document.getElementById('pie_chosen'));		
	chart.draw(data, options);	
	
	// draw deficit pie
	var data_d = new google.visualization.DataTable();
	var deficit = expenditure - fat - protein - carbs;
	if (deficit < 0) {
		deficit = 0;
	}
	data_d.addColumn('string', 'Ratio');
	data_d.addColumn('number', 'Calories');
	data_d.addRow(['Deficit Calories', deficit]);
	
	var deficit_ratio = Math.sqrt(deficit)/Math.sqrt(expenditure);
	var options_d = {
		'chartArea': {
			'width':176*deficit_ratio,
			'height':176*deficit_ratio
		},
		'width':176*deficit_ratio + 26,
		'height':176*deficit_ratio + 26,
		'colors':['#264A73'],
		'legend':'none',
		'fontSize':10,
		'pieSliceText':'value'
	};
	
	var chart_d = new google.visualization.PieChart(document.getElementById('pie_deficit'));
	chart_d.draw(data_d, options_d);
}


function draw_chart(weight_table) {
	var table = weight_table[0];
	var current_weight_table_input = weight_table[1];

	// find out if kg or lbs
	var doc = document.data;
	
	var is_checked = doc.chart_weight_type[0].checked || doc.chart_weight_type[1].checked
	var graphstartdate = doc.graphstartdate.value;
		
	if (is_checked && table.length > 1 && google_is_loaded_bool && graphstartdate != "") {
		var start_date = new Date(graphstartdate);
	
		var is_lbs = parseInt(radio_val(doc.chart_weight_type), 10);
		
		var type = "kg";
		var fact = 1.0;
		
		if (is_lbs) {
			type = "lbs";
			fact = 1.0/0.45359237;
		}
		
		current_weight_table_input.push(fact);
		current_weight_table_input.push(start_date.getTime());
		
		// check if the weight tables are very similar, and only redraw if not
		if (!is_similar(current_weight_table_input, last_weight_table_input, 0.00001)) {
			last_weight_table_input = current_weight_table_input;
		
			// convert table to DataTable
			var data = new google.visualization.DataTable();
			data.addColumn('date', 'Date');
			data.addColumn('number', "Weight [" + type + "]");
			data.addColumn('string', 'title1');
			data.addColumn('string', 'text1');
			data.addColumn('number', "Bodyfat [" + type + "]");
			data.addColumn('string', 'title1');
			data.addColumn('string', 'text1');
			
			var d = start_date;
			var min_kcal_reached = false;
			var min_weight_reached = false;
			var prev_bodyfat_percent = 100 * table[0][1] / table[0][0];
			for (var i=0; i<table.length; ++i) {
				var t = table[i];
				
				var title_w = null;
				var text_w = null;
				var title_bf = null;
				var text_bf = null;
				
				if (t[3] < t[2] && !min_kcal_reached) {
					min_kcal_reached = true;
					title_w = 'min kcal reached';
					text_w = "Starting from " + (d.getMonth()+1) + "/" + d.getDate() + "/" + d.getFullYear() + ", you need to increase your calorie intake to prevent muscle loss. Assuming increased intake from here on!";
				}
				
				if (t[4] == 0 && !min_weight_reached) {
					min_weight_reached = true;
					title_w = 'min weight reached';
					text_w = "Starting from " + (d.getMonth()+1) + "/" + d.getDate() + "/" + d.getFullYear() + ", you can not lose any more fat. Assuming maintenance intake from here on!";
				}
				
				// calculate bodyfat %
				var bodyfat_percent = 100 * t[1] / t[0];
				if (Math.floor(bodyfat_percent/5) < Math.floor(prev_bodyfat_percent/5)) {
					var actual_percent = Math.floor(prev_bodyfat_percent);
					title_bf = "" + actual_percent + "%";
					text_bf = "On " + (d.getMonth()+1) + "/" + d.getDate() + "/" + d.getFullYear() + ", below " +  actual_percent + "% bodyfat";
				}
				prev_bodyfat_percent = bodyfat_percent;
				
				data.addRow([new Date(d.getTime()), t[0]*fact, title_w, text_w, t[1]*fact, title_bf, text_bf]);
				d.setDate(d.getDate() + 1);
			}
			
			var annotatedtimeline = new google.visualization.AnnotatedTimeLine(
			  document.getElementById('chart'));
			annotatedtimeline.draw(data, { 'displayAnnotations': true, 'min': 0 });
		}
	}
	
	check_adblocker();	
}

function use_graphstartdate_today() {
	var d = document.data;
	var date = new Date();
	d.graphstartdate.value = (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() ;
	
	// recalculate
	calc_handler(null);
}

function select_all_handler(e) {
	e.target.select();
}

// Add event listeners once the DOM has fully loaded by listening for the
// `DOMContentLoaded` event on the document, and adding your listeners to
// specific elements when it triggers.
document.addEventListener('DOMContentLoaded', function () {	
	var elem = document.data;
	for (var i=0; i<elem.length; ++i) {
		if (elem[i] != document.data.reddit_copypaste) {
			elem[i].addEventListener('keyup', calc_handler);
			elem[i].addEventListener('click', calc_handler);
		} else {
			document.data.reddit_copypaste.addEventListener('click', select_all_handler);
		}
	}

},
false);


// exports for compression: store the function in a global property referenced by a string:
window['toggle_visibility'] = toggle_visibility;
window['use_graphstartdate_today'] = use_graphstartdate_today;
window['load_cookie'] = load_cookie;
window['mark_empty_fields'] = mark_empty_fields;
window['google_is_loaded'] = google_is_loaded;
