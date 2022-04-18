'use strict'

const url = window.location.href
let data
const formBox = document.getElementById('quiz-box')
const resultBox = document.getElementById('result-box')
console.log(resultBox)
const scoreBox = document.getElementById('score-box')
console.log(scoreBox)
console.log(formBox)


$.ajax({
	method: "GET",
	url: `${url}data`,
	success: function (response) {
		data = response.data
		data.forEach(el => {

			for (const [questions, answers] of Object.entries(el)) {

				formBox.innerHTML += `

					<hr>
					<div class="mb-2">
						<b>${questions}</b>
					</div>
				`

				answers.forEach(answer => {
					formBox.innerHTML += `
						<div>
						<input type="radio" name="${questions}" class="ans" id="${questions} - ${answer}" value="${answer}">
						<label for="${questions}"> ${answer} </label>
						</div>
					`
				});
			}

		});
	},
	error: function (error) {
		console.log(error)
	}
})

const quizForm = document.getElementById('form-quiz')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {

	const elements = [...document.getElementsByClassName('ans')]
	const data = {}
	data['csrfmiddlewaretoken'] = csrf[0].value
	elements.forEach(el => {

		if (el.checked) {
			data[el.name] = el.value
		}
		else {

			if (!data[el.name]) {
				data[el.name] = null
			}
		}
	});

	$.ajax({
		type: 'POST',
		url: `${url}save/`,
		data: data,
		success: function (response) {
			const results = response.results;
			console.log(results);
			quizForm.classList.add('not-visible');
			const score_final = `${response.score.toFixed(2)}`
			scoreBox.innerHTML = `${response.passed ? "Congratulations" : "Please Try Again!"} Your result is ${score_final}`
			if(score_final == 60){
			    scoreBox.innerHTML += " Good Job!";
			}
			else if(score_final == 80){
			    scoreBox.innerHTML += " Excellent Work!";
			}
			else if(score_final == 100){
			    scoreBox.innerHTML += " You are a genius!";
			}
		},
		error: function (response) {
			console.log(response)
		}
	});
}

quizForm.addEventListener('submit', e => {
	e.preventDefault()
	sendData()
});