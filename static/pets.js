const BASE_URL = "https://api.petfinder.com/v2/animals";
const url = "http://127.0.0.1:5000";
const API_CLIENT_KEY = "56echxaStqqEbshW5qM7UiIDncLPF96oxy7BXnSGaIublt9wf4";
const API_SECRET_KEY = "cBpMYemJe2WziCouYm7eoKGbYdH5VaoSwlI0NcIu";
// let petCard = document.querySelector("#pets");
let $petCard = $("#pets");
const $showPets = $("#show-pets");
let $imgSrc;
const default_image =
  "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif";

let pf = new petfinder.Client({
  apiKey: API_CLIENT_KEY,
  secret: API_SECRET_KEY,
});

async function renderPets(p) {
  for (let i = 0; i < p.length; i++) {
    if (p[i].photos.length === 0) {
      $imgSrc = default_image;
    } else {
      $imgSrc = p[i].photos[0].small;
    }
    let pet = `<div class="card text-center m-1" style="width: 18rem">
    <img src="${$imgSrc}" class="card-img-top m-1 img" alt="image of pets">
    <div class="card-body pet-card">
    <div class="pet-name-container">
      <h5 class="card-title">${p[i].name}</h5>
      <a href="${url}/favorite/${p[i].id}" class="btn btn-outline-danger" data-pet=${p[i].id}><i class="fa fa-heart"></i></a>
    </div>
    <p class="card-text">${p[i].gender}</p>
    <p class="card-text">${p[i].type}</p>
    <a href="${url}/pet/${p[i].id}" id="pet-info-button" class="btn btn-outline-dark" data-pet=${p[i].id}>About me!</a>
    </div>
    </div>`;
    $petCard.append(pet);
  }
}

$showPets.click(function () {
  const data = JSON.parse(localStorage.getItem("pets"));
  renderPets(data);
});

function handleResponse() {
  pf.animal
    .search()
    .then(function (response) {
      localStorage.setItem("pets", JSON.stringify(response.data.animals));
    })
    .catch(function (error) {
      console.log(error);
    });
}

handleResponse();
