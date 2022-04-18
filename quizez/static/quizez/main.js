'use strict'

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

console.log(startBtn)

const url = window.location.href

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
	const pk = modalBtn.getAttribute('data-pk')
	const name = modalBtn.getAttribute('data-quiz')
	const ques = modalBtn.getAttribute('data-questions')
	const pass = modalBtn.getAttribute('data-pass')

	console.log(name)

	modalBody.innerHTML = `

	<div class="h5" mb-3"> Quiz for ${name}</div>
	<div class="text-muted">
	<ul>
		<li> Number Of Questions: <b> ${ques} </b> </li>
		<li> Required Score To Pass:  <b> ${pass}</b>% </li>
	</ul>
	</div>
    `
	startBtn.addEventListener('click', () => {
		window.location.href = url + pk
	})
}))