<template>
  <div>
    <div v-for="voter in players" :key="voter.id">
              {{voter.name}} assigned tokens: {{ voter.betAmount }} {{
              voter.betAmount > 0
              ? "🔥".repeat(voter.betAmount) : "💀".repeat(Math.abs(voter.betAmount)) }}
         <b-form-input :name="voter.name"
                            :key="voter.name"
                            id="form-votes-input"
                            type="range"
                            placeholder=0
                            min=-5
                            max=5
                            value="0"
                            step=1
                            v-model.number="voter.betAmount">
      </b-form-input>
    </div>

  </div>
</template>

<script>
export default {
  props: ['players'],
};
</script>
