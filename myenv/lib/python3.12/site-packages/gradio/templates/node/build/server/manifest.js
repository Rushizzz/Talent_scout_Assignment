const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.BaRWwSYh.js","app":"_app/immutable/entry/app.C2gir6b8.js","imports":["_app/immutable/entry/start.BaRWwSYh.js","_app/immutable/chunks/client.BM2WibkS.js","_app/immutable/entry/app.C2gir6b8.js","_app/immutable/chunks/preload-helper.DpQnamwV.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-Bk3RF1fr.js')),
			__memo(() => import('./chunks/1-ComljbxZ.js')),
			__memo(() => import('./chunks/2-NDW0dV-l.js').then(function (n) { return n.aC; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
