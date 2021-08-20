import 'highlight.js/styles/github.css';
import 'higlass/dist/hglib.css';
import { embed } from 'gosling.js';

embed(document.getElementById('root'), window.SPEC || {}, { padding: 0 });
