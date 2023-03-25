const spinButton = document.getElementById("spin-button");
const wheel = document.getElementById("wheel");

const foodName = document.getElementById("food-name");
const description = document.getElementById("description");
const price = document.getElementById("price");
const restaurantName = document.getElementById("restaurant-name");

let spinsLeft = 100;

function displayResult(item) {
	//add each item in span tag before displaying
	document.querySelector(".food_name_span").textContent = item.FoodName;
	document.querySelector(".description_span").textContent = item.Description;
	document.querySelector(".price_span").textContent = item.Price + " AED";
	document.querySelector(".restaurant_name_span").textContent =
		item.RestaurantName;
	document
		.querySelector(".restaurant_name_span")
		.classList.add("alert", "alert-info");
}

spinButton.addEventListener("click", () => {
	if (spinsLeft > 0) {
		// Rotate the wheel by a random number of degrees
		const randomDegrees = Math.floor(Math.random() * 360) + 720;
		wheel.style.transform = `rotate(-${randomDegrees}deg)`;
		// Decrement the number of spins left
		spinsLeft--;

		// Call the fetch function every 99 milliseconds while the wheel is spinning
		const intervalId = setInterval(() => {
			fetch("/spin")
				.then((response) => response.json())
				.then((item) => {
					displayResult(item);
				});
		}, 60);

		// After 6 seconds, stop the wheel and clear the interval ID
		setTimeout(() => {
			// Stop the spinning and clear the interval ID
			wheel.style.transform = "none";
			clearInterval(intervalId);
			// spinButton.disabled = true;
			// spinButton.textContent = "No spins left";
		}, 1000);

		// Display the number of spins left
	}
});

foodName.addEventListener("click", (e) => {
	e.AT_TARGET;
	const foodName = e.target.innerText.trim();
	// show loading spinner
	const restaurantName = document.querySelector(
		".restaurant_name_span"
	).innerText;

	const price = document.querySelector(".price_span").innerText;

	const food_restaurant_price = foodName + ":" + restaurantName + ":" + price;

	const loading_spinner = document.querySelector(".loading-spinner");
	loading_spinner.style.display = "flex";
	//disable the button by changing the color
	// foodName.classList.add("disabled");
	fetch(`/search/${food_restaurant_price}`)
		.then((response) => response.json())
		.then((item) => {
			displayNutritionModal(item);
			// remove loading spinner
			loading_spinner.style.display = "none";
		})
		.catch((error) => {
			console.log(error);
		});
});

function displayNutritionModal(foodItem) {
	const modal = document.querySelector(".modal");
	const modalContent = modal.querySelector(".modal-content");
	const modalFooterContent = modal.querySelector(".modal-footer-content");
	const modalFooterTitle = modal.querySelector(".modal-footer-title h6");
	console.log(foodItem["nutrition_facts"]);
	nutritionFacts = JSON.parse(foodItem["nutrition_facts"]);
	// console.log(foodItem["similar_food"]);
	//check foodItem["similar_food"] is not empty using empty array
	// add similar food to the footer as bootsrap cards
	if (foodItem["similar_food"].length) {
		similarFood = JSON.parse(foodItem["similar_food"]);
		modalFooterContent.innerHTML = "";
		console.log(similarFood);
		modalFooterTitle.textContent = "Similar Foods At A Cheaper Price";
		similarFood.forEach((food) => {
			const card = document.createElement("div");
			card.classList.add("card", "col-3", "m-2");
			const cardBody = document.createElement("div");
			cardBody.classList.add("card-body");
			const cardTitle = document.createElement("h5");
			cardTitle.classList.add("card-title");
			cardTitle.textContent = food.FoodName + "🍔";
			const cardText = document.createElement("p");
			cardText.classList.add("card-text", "badge", "badge-dark");
			cardText.textContent = food.RestaurantName + "👨🏽‍🍳";
			// cardText.addClassList("badge", "badge-dark");
			const cardPrice = document.createElement("p");
			cardPrice.classList.add("card-text");
			cardPrice.textContent = food.Price + " AED 🤑";
			cardBody.appendChild(cardTitle);
			cardBody.appendChild(cardText);
			cardBody.appendChild(cardPrice);
			card.appendChild(cardBody);
			modalFooterContent.appendChild(card);
		});
	}

	const heading = modalContent.querySelector("h2");
	heading.textContent = nutritionFacts.name;

	const classification = modalContent.querySelector(".classification");
	classification.textContent = nutritionFacts.classification;
	//if classification is "indulgetnt" then make the text red
	if (nutritionFacts.classification === "indulgent") {
		classification.classList.add("badge", "badge-danger", "text-white");
	} else {
		classification.classList.add("badge", "badge-success", "text-white");
	}
	//Update the classification tex to be Title Case
	classification.textContent = classification.textContent.replace(
		/indulgent|healthy/gi,
		(match) => match[0].toUpperCase() + match.slice(1)
	);

	const nutritionData = nutritionFacts.hasOwnProperty("nutrition")
		? nutritionFacts.nutrition
		: nutritionFacts["Nutritional Facts"]?.[0];

	const nutritionList = modalContent.querySelector(".nutrition-list");
	nutritionList.innerHTML = ""; // Clear existing list items

	if (nutritionData) {
		for (const prop in nutritionData) {
			const listItem = document.createElement("li");
			listItem.textContent = `${prop}: ${nutritionData[prop]}`;
			listItem.classList.add(
				"list-group-item",
				"d-flex",
				"justify-content-between",
				"align-items-center"
			);
			nutritionList.appendChild(listItem);
		}
	}

	modal.style.display = "block";
}

// Add an event listener for the close button
const modal = document.querySelector(".modal");
const closeButton = modal.querySelector(".close");
closeButton.addEventListener("click", () => {
	modal.style.display = "none";
});
