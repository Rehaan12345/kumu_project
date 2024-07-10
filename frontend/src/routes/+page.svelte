<script>
    import { onMount } from "svelte";
    import { Input, Label, Helper, Button, Checkbox, A } from 'flowbite-svelte';

    // Function to accept the inputted "TO"s and send them here.

    let tags = [];
    let row = -1;
    let col_ind = -1;

    async function createLabel(description, label, tag_s, type) {

        tags.push(tag_s);

        const toSend = {
            description,
            label,
            tags,
            type
        }; // Make sure the values here match the ORDER and NAME that is expected in the Python class!

        console.log(toSend)

        try {
            const url = "http://127.0.0.1:8000/createlabel/"; 
            const res = await fetch(url, {
                method: "POST",
                headers: {"Content-type": "application/json"},
                body: JSON.stringify(toSend)
            });
            const resData = await res.json();
            const msg = resData["status"];
            console.log("Successfully retrieved message: " + msg);
            location.reload(); // Change later, etc.
        } catch (error) {
            console.log("Error: " + error);
        }
    }

    async function linkElements(fromelement, toelement) {
        // Along the way multiple toelements can be selected, and thus the variable parameter toelement here will be an array. -> This has not yet been implemented and toelement is currently just a string.
        const vals = [];
        vals.push(fromelement); // values[0] will always be the FROM element.
        vals.push(toelement);
        // console.log("fromel: " + fromelement + "\ntoel: " + toelement);
        console.log(vals);
        const row = -1;
        const col_ind = 0;

        const toSend = {
            vals,
            row,
            col_ind
        }

        console.log(toSend);

        try {
            const url = "http://127.0.0.1:8000/linkdocs/";
            const res = await fetch(url, {
                method: "POST",
                headers: {"Content-type": "application/json"},
                body: JSON.stringify(toSend)
            });
            const resData = await res.json();
            const status = resData["status"];
            console.log("Status: " + status);
            location.reload(); // Change later, etc.
        } catch (error) {
            console.log("Error: " + error);
        }
    }

    let labels = []

    async function getLabels() {
        try {
            const url = "http://127.0.0.1:8000/getvals/" + "Elements/";
            const res = await fetch(url);
            if (!res.ok) { throw new Error("getvals fetching didn't work"); }
            const resData = await res.json();
            labels = resData["status"];
            console.log(labels);
            return labels;
        } catch (error) {
            console.log("Couldn't retrieve / fetch getvals data: " + error);
        }
    }

    // let labels;

    onMount(() => {
        getLabels();
        console.log(labels);
    })

</script>

<div class="maincontainer">
    <div class="mainformcontainer">
        <div class="createlabeltitle">Create Label</div>
        <div class="createlabelformcontainer">
            <form on:submit={() => {
                const description = document.querySelector(".description").value;
                const label = document.querySelector(".label").value;
                const tags = document.querySelector(".tags").value;
                const type = document.querySelector(".type").value;
                createLabel(description, label, tags, type);
            }}>
            <div class="grid gap-6 mb-6 md:grid-cols-2">
                <div>
                    <Label for="description" class="mb-2">Description</Label>
                    <Input type="text" id="description" class="description" placeholder="New element" required />
                </div>
                <div>
                    <Label for="label" class="mb-2">Label</Label>
                    <Input type="text" id="label" class="label" placeholder="Label" required />
                </div>
                <div>
                    <Label for="tags" class="mb-2">Tags</Label>
                    <Input type="text" id="tags" class="tags" placeholder="Tag"/>
                </div>
                <div>
                    <Label for="type" class="mb-2">Type</Label>
                    <Input type="text" id="type" class="type" placeholder="Type"/>
                </div>
            </div>
            <Button type="submit">Create Label</Button>
            </form>
        </div>
        <div class="linkelementstitle">Link Elements</div>
        <form on:submit={() => {
            const fromelement = document.querySelector(".selectfrom").value;
            const toelement = document.querySelector(".selectto").value;
            linkElements(fromelement, toelement);
        }} class="linkelementsform">
            <Label for="fromelement">From</Label>
            <select class="selectfrom" name="fromelement">
                <option value="Select">Select</option>
                {#each labels as label}
                    <option class="fromelement" value={label[0]}>{label[0]}</option>
                {/each}
            </select>
            <Label for="toelement">To</Label>
            <select class="selectto" name="toelement">
                <!-- Down the line can select multiple, and pass them as an array, etc. -> This hasn't yet been implemented. -->
                <option value="Select">Select</option>
                {#each labels as label}
                    <option class="toelement" value={label[0]}>{label[0]}</option>
                {/each}
            </select>
            <Input type="submit" value="Link"/>
        </form>

    </div>

    <div class="kumucontainer">
        <iframe title="kumumap" src="https://embed.kumu.io/e67ccd8bba0bf9409a9a4b9fa572aa7b" width="940" height="600" frameborder="0"></iframe>
    </div>

</div>

<style>
    .createlabelformcontainer {
        /* border: 4px solid black; */
        display: flex;
        max-width: 30rem;
        justify-content: space-between;
    }
</style>