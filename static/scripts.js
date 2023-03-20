const spinButton = document.getElementById("spin-button");
const wheel = document.getElementById("wheel");

const foodName = document.getElementById("food-name");
const description = document.getElementById("description");
const price = document.getElementById("price");
const restaurantName = document.getElementById("restaurant-name");

let spinsLeft = 100;

function displayResult(item) {
	foodName.textContent = "Food Name: " + item.FoodName;
	description.textContent = "Description: " + item.Description;
	price.textContent = "Price: " + item.Price;
	restaurantName.textContent = "Restaurant Name: " + item.RestaurantName;
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
// Get the elements
const dropdown = document.querySelector("#restaurant-picker .dropdown");
const dropdownMenu = document.querySelector(
	"#restaurant-picker .dropdown-menu"
);
const dropdownButton = document.querySelector(
	"#restaurant-picker .dropdown-toggle"
);
const dropdownItems = dropdownMenu.querySelectorAll(".dropdown-item");

// Add event listener to the button
dropdownButton.addEventListener("click", function () {
	dropdown.classList.toggle("active");
	dropdownMenu.classList.toggle("active");
});

// Add event listeners to the dropdown items
dropdownItems.forEach(function (item) {
	item.addEventListener("click", function () {
		dropdownItems.forEach(function (item) {
			item.classList.remove("active");
		});
		this.classList.add("active");
		dropdownButton.innerHTML =
			this.textContent + ' <span class="caret"></span>';
	});
});
