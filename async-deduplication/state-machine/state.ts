import {createMachine} from 'xstate';

enum Action {
    logProcessingOrder = 'logProcessingOrder',
    logCompletingOrder = 'logCompletingOrder'
}

export const orderStateMachine = createMachine({
  id: 'order',
  initial: 'new',
  states: {
    new: {
      on: {
        PROCESS: {
            target: 'processing',
            actions: [Action.logProcessingOrder]
        },
      }
    },
    processing: {
      on: {
        COMPLETE: {
            target: 'completed',
            actions: [Action.logCompletingOrder]
        },
      }
    },
    completed: {
      // No transitions out of completed in this simple example
      type: 'final'
    }
  }
}, {
    actions: {
        [Action.logProcessingOrder]: (ctx, event) => {
            console.log('Processing order')
        },
        [Action.logCompletingOrder]: (ctx, event) => {
            console.log('Completing order')
        }
    }
});
