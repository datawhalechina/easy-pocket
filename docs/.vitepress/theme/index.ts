import DefaultTheme from 'vitepress/theme'
import './custom.css'
import type { Theme } from 'vitepress'
import 'viewerjs/dist/viewer.min.css';
import imageViewer from 'vitepress-plugin-image-viewer';
import vImageViewer from 'vitepress-plugin-image-viewer/lib/vImageViewer.vue';
import { useRoute } from 'vitepress';
import Layout from './Layout.vue'
import HomePortal from './components/HomePortal.vue'

export default {
    extends: DefaultTheme,
    Layout,
    enhanceApp({ app }) {
        app.component('vImageViewer', vImageViewer);
        app.component('HomePortal', HomePortal);
    },
    setup() {
        const route = useRoute();
        imageViewer(route);
    },
} satisfies Theme
