import { createActor } from "xstate";
import { orderStateMachine } from "./state";

// Interpret the machine to create a service
const orderActor = createActor(orderStateMachine)
  .start();

orderActor.subscribe((state) => {
    console.log('Subscribe state change: ' + state.value);
});

// Simulating order processing
console.log("Attempting to process a new order...");
orderActor.send({type: 'PROCESS'});

console.log("Attempting to complete the order...");
orderActor.send({type: 'COMPLETE'});

// Attempting idempotent operations
console.log("Attempting to process an already completed order...");
orderActor.send({type: 'PROCESS'}); // This will have no effect

console.log("Attempting to complete an already completed order...");
orderActor.send({type: 'COMPLETE'}); // This will also have no effect