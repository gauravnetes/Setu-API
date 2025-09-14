<script lang="ts">
	import jsPDF from 'jspdf';
	import type { Diagnosis } from '$lib/types';
	import { selectedDiagnosis } from '$lib/store';
	import SearchResultCard from '$lib/SearchResultCard.svelte';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';

	// Your existing logic is perfect. This subscribes to the store.
	let diagnosis = $selectedDiagnosis;
	let showModal = false;

	// This guard clause is excellent. It prevents direct access.
	onMount(() => {
		if (!diagnosis) {
			goto('/');
		}
	});

	// BEST PRACTICE: Clean up the store when the user navigates away.
	onDestroy(() => {
		selectedDiagnosis.set(null);
	});

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			showModal = false;
		}
	}

	function downloadReport(diagnosis: Diagnosis) {
		if (!diagnosis) return;
		const doc = new jsPDF();

		// Title
		doc.setFontSize(16);
		doc.text('Patient Electronic Medical Record', 10, 20);

		// Patient details
		doc.setFontSize(12);
		doc.text('Patient: Anjali Sharma, 34F', 10, 40);
		doc.text('Record #: 789-456-123', 10, 50);

		// Encounter note
		doc.text('Encounter Note - 14 Sep 2025', 10, 70);

		doc.text(
			'S (Subjective): Patient reports radiating pain down the right leg, worse when sitting. Denies injury.',
			10,
			90
		);
		doc.text(
			'O (Objective): Positive Straight Leg Raise test on right. Vitals stable. Ayurvedic exam suggests Vata aggravation.',
			10,
			100
		);

		// ✅ Safe access with nullish coalescing
		doc.text(`A (Assessment):`, 10, 115);
		doc.text(`Diagnosis Added: ${diagnosis.Traditional_Term ?? 'N/A'}`, 10, 125);

		const setuLink: string = diagnosis.SETU_Link ?? 'https://setu.example.com';
		doc.textWithLink('View SETU Link', 10, 135, { url: setuLink });

		doc.text(
			'P (Plan): 1. Prescribe Ayurvedic formulations. 2. Advise Yogasanas. 3. Follow-up in 2 weeks.',
			10,
			150
		);

		// Save file
		doc.save('emr_report.pdf');
	}
</script>

<main class="min-h-screen bg-gray-100 p-4 font-sans md:p-8">
	<div class="mx-auto max-w-4xl rounded-lg bg-white p-6 shadow-2xl md:p-8">
		<button
			type="button"
			class="mb-2 cursor-pointer text-lg font-bold text-sky-400"
			on:click={() => history.back()}
		>
			← Back
		</button>

		<div class="mb-6 border-b border-gray-200 pb-4">
			<h1 class="text-3xl font-bold text-gray-800">Patient Electronic Medical Record</h1>
			<div class="mt-2 flex justify-between text-sm text-gray-600">
				<span><strong>Patient:</strong> Anjali Sharma, 34F</span>
				<span><strong>Record #:</strong> 789-456-123</span>
			</div>
		</div>

		<div>
			{#if diagnosis}
				<button
					type="button"
					class="cursor-pointer rounded-full bg-sky-100 px-5 py-3 text-xs font-semibold text-sky-800 transition-colors duration-500 hover:bg-sky-300 hover:text-zinc-800"
					on:click={downloadReport}
				>
					Download EMR Report (PDF)
				</button>
			{/if}
			<h2 class="mb-4 text-xl font-semibold text-gray-700">Encounter Note - 14 Sep 2025</h2>

			<div class="space-y-6">
				<div>
					<h3 class="font-bold text-gray-800">S (Subjective)</h3>
					<p class="mt-1 border-l-2 pl-4 text-gray-600">
						Patient reports radiating pain down the right leg, worse when sitting. Denies injury.
					</p>
				</div>

				<div>
					<h3 class="font-bold text-gray-800">O (Objective)</h3>
					<p class="mt-1 border-l-2 pl-4 text-gray-600">
						Positive Straight Leg Raise test on right. Vitals stable. Ayurvedic exam suggests Vata
						aggravation.
					</p>
				</div>

				<div>
					<h3 class="font-bold text-gray-800">A (Assessment)</h3>
					{#if diagnosis}
						<div class="mt-2 rounded-r-lg border-l-4 border-green-400 bg-green-50 p-4">
							<h3 class="text-lg font-bold text-green-600">
								Diagnosis Added: {diagnosis.Traditional_Term}
							</h3>
							<p class="mt-2 text-gray-700">
								The following diagnosis has been added to the patient's problem list based on the
								SETU API mapping.
							</p>
							<button
								on:click={() => (showModal = true)}
								class="mt-4 font-semibold text-sky-600 hover:underline"
							>
								View SETU Link Details
							</button>
						</div>
					{:else}
						<p class="border-l-2 pl-4 text-gray-500">
							No diagnosis has been added in this session.
						</p>
					{/if}
				</div>

				<div>
					<h3 class="font-bold text-gray-800">P (Plan)</h3>
					<p class="mt-1 border-l-2 pl-4 text-gray-600">
						1. Prescribe Ayurvedic formulations. 2. Advise Yogasanas. 3. Follow-up in 2 weeks.
					</p>
				</div>
			</div>
		</div>
	</div>
</main>

{#if showModal && diagnosis}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
		<!-- Backdrop as a real button -->
		<button
			type="button"
			class="absolute inset-0 h-full w-full cursor-default"
			aria-label="Close modal"
			on:click={() => (showModal = false)}
			on:keydown={handleKeydown}>hello</button
		>

		<!-- Modal content -->
		<div class="relative w-full max-w-4xl" role="presentation" on:click|stopPropagation>
			<SearchResultCard result={diagnosis} showAddButton={false} />
		</div>
	</div>
{/if}
