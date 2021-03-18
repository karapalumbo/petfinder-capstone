const BASE_URL = "https://api.petfinder.com/v2/animals";
const API_CLIENT_KEY = "56echxaStqqEbshW5qM7UiIDncLPF96oxy7BXnSGaIublt9wf4";
const API_SECRET_KEY = "cBpMYemJe2WziCouYm7eoKGbYdH5VaoSwlI0NcIu";
const petForm = $("#pet-form");
let petCard = $("#pets");
const default_image =
  "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif";

let pf = new petfinder.Client({
  apiKey: API_CLIENT_KEY,
  secret: API_SECRET_KEY,
});

function renderPets(pets) {
  for (let i = 0; i < pets.length; i++) {
    console.log(pets[i]);
    let pet = `<div class="card m-1" style="width: 18rem;">
    <img src="${default_image}" class="card-img-top m-1" alt="image of pets">
    <div class="card-body">
    <h5 class="card-title">${pets[i].name}</h5>
    <p class="card-text">${pets[i].type}</p>
    <a href="#" class="btn btn-primary">About me!</a>
    </div>
    </div>`;
    petCard.append(pet);
  }
}

function handleResponse(evt) {
  evt.preventDefault();
  pf.animal
    .search()
    .then(function (response) {
      renderPets(response.data.animals);
    })
    .catch(function (error) {
      console.log(error);
    });
}

$("#pet-form").on("submit", handleResponse);
