const modal = document.getElementById('modal')

document.getElementById('openModal').onclick = () => modal.classList.remove('hidden')
document.getElementById('closeModal').onclick = () => modal.classList.add('hidden')

const step1 = document.getElementById('step1')
const step2 = document.getElementById('step2')
const step3 = document.getElementById('step3')

const step1Tab = document.getElementById('step1Tab')
const step2Tab = document.getElementById('step2Tab')
const step3Tab = document.getElementById('step3Tab')

document.getElementById('toStep2').onclick = () => {
    step1.classList.add('hidden')
    step2.classList.remove('hidden')
    step1Tab.classList.replace('bg-blue-900', 'bg-gray-300')
    step1Tab.classList.replace('text-white', 'text-gray-600')
    step2Tab.classList.replace('bg-gray-300', 'bg-blue-900')
    step2Tab.classList.replace('text-gray-600', 'text-white')
}

document.getElementById('toStep3').onclick = () => {
    step2.classList.add('hidden')
    step3.classList.remove('hidden')
    step2Tab.classList.replace('bg-blue-900', 'bg-gray-300')
    step2Tab.classList.replace('text-white', 'text-gray-600')
    step3Tab.classList.replace('bg-gray-300', 'bg-blue-900')
    step3Tab.classList.replace('text-gray-600', 'text-white')
}

document.getElementById('backTo1').onclick = () => {
    step2.classList.add('hidden')
    step1.classList.remove('hidden')
    step2Tab.classList.replace('bg-blue-900', 'bg-gray-300')
    step2Tab.classList.replace('text-white', 'text-gray-600')
    step1Tab.classList.replace('bg-gray-300', 'bg-blue-900')
    step1Tab.classList.replace('text-gray-600', 'text-white')
}

document.getElementById('backTo2').onclick = () => {
    step3.classList.add('hidden')
    step2.classList.remove('hidden')
    step3Tab.classList.replace('bg-blue-900', 'bg-gray-300')
    step3Tab.classList.replace('text-white', 'text-gray-600')
    step2Tab.classList.replace('bg-gray-300', 'bg-blue-900')
    step2Tab.classList.replace('text-gray-600', 'text-white')
}