<script>
    import { onMount } from "svelte";
    import { Input, Label, Helper, Button, Checkbox, A } from 'flowbite-svelte';

    // Function to accept the inputted "TO"s and send them here.

    let vals = [];
    let row = -1;
    let col_ind = -1;

    async function sendData(from, to) {

        vals.push(from);
        vals.push(to)
        row = 1; // Specify this in the form later.
        col_ind = 0; // Specify this in the form later.

        const toSend = {
            vals,
            row,
            col_ind
        }; // Make sure the values here match what is expected in the Python code!

        console.log("values: " + vals + "\nrow: " + row + "\ncol_ind: " + col_ind);
        console.log(toSend)

      try {
          const url = "http://127.0.0.1:8000/updatevals/"; 
          const res = await fetch(url, {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(toSend)
          });
          const resData = await res.json();
          const msg = resData["status"];
          console.log("Successfully retrieved message: " + msg);
          location.reload();
      } catch (error) {
          console.log("Error: " + error);
      }
    }

</script>

<div class="maincontainer">
    <div class="mainformcontainer">
        <form on:submit={() => {
            const from = document.querySelector(".from").value;
            const to = document.querySelector(".to").value;
            sendData(from, to);
        }}>
        <div class="grid gap-6 mb-6 md:grid-cols-2">
            <div>
            <Label for="first_name" class="mb-2">From</Label>
            <Input type="text" id="first_name" class="from" placeholder="John" required />
            </div>
            <!-- Ask for dropdown "how many 'TO's do you want to add, then dynamically increase the amount of inputs to accept all of these 'TO's and then send them as a list to the backend to be processed." -->
            <div>
            <Label for="last_name" class="mb-2">To</Label>
            <Input type="text" id="last_name" class="to" placeholder="Doe" required />
            </div>
        </div>
        <Button type="submit">Update</Button>
        </form>
    </div>

    <div class="kumucontainer">
        <iframe title="kumumap" src="https://embed.kumu.io/e67ccd8bba0bf9409a9a4b9fa572aa7b" width="940" height="600" frameborder="0"></iframe>
    </div>

</div>