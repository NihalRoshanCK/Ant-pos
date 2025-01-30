<template>
    <div class="bg-gray-300 w-screen h-full flex items-center justify-between p-4">
        <div class="flex gap-4 items-center">
            <div>
                <FeatherIcon name="menu" class="w-5 h-5"/>
            </div>
            <div class="flex text-center gap-3  items-center">
                <img src="" class="w-8 h-8" alt="logo">
                <p class="text-xl ">
                    Ant-Pos 
                </p>
            </div>
            <!-- <div>
                
            </div> -->
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