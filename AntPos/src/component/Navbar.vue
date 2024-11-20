<template>
    <div class="bg-gray-300 w-screen h-full flex items-center justify-between p-4">
        <div class="flex gap-4">
            <div>
                han
            </div>
            <div>
                Ant-Pos 
            </div>
        </div>
        <div class="flex gap-4">
            <div>
                {{base?.Ant_Opening_Shift?.pos_profile}}
            </div>
                <Dropdown
                    :options="[
                        {
                        label: 'Close Shift',
                        onClick: () => {
                                    },
                        icon: () => h(FeatherIcon, { name: 'file-minus' }),
                        },
                        {
                        label: 'Logout',
                        onClick: () => {
                                    },
                        icon: () => h(FeatherIcon, { name: 'log-out' }),
                        },
                    ]"
                    :button="{
                        label: 'Menu',
                    }"
                />
        </div>
    </div>
</template>

<script setup>
    import { h , inject } from 'vue'; 

    const base = inject('base')

    import { Dropdown , FeatherIcon } from 'frappe-ui'
</script>