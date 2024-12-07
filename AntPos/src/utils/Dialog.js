import { ref } from 'vue';

export function useDynamicComponent() {
    const currentComponent = ref(null);

    const loadComponent = async (componentName) => {
        try {
            const components = {
                OpenShift: () => import('../component/Dialog/Open-Shift.vue'),
                CustomerForm: () => import('../component/Dialog/CustomerForm.vue'),
            };

            if (components[componentName]) {
                const component = await components[componentName]();
                currentComponent.value = component.default;
            } else {
                console.error(`Component "${componentName}" not found.`);
                currentComponent.value = null;
            }
        } catch (error) {
            console.error('Error loading component:', error);
            currentComponent.value = null;
        }
    };

    return { currentComponent, loadComponent };
}