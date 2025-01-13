import type { LinksFunction } from "@remix-run/node";
import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";
import { MainNav, MobileNav } from "./components/ui/nav";
import globalStylesUrl from "./styles/globals.css?url";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: globalStylesUrl },
];

export default function App() {
  return (
    <html lang="ja">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <div className="layout-grid">
          <header className="header bg-white border-b border-gray-200 px-4 flex items-center justify-between">
            <h1 className="text-xl font-semibold text-gray-800">Scale App</h1>
            <div className="flex items-center space-x-4">
              <button className="text-gray-500 hover:text-gray-700">
                <span className="sr-only">通知</span>
                <svg
                  className="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                  />
                </svg>
              </button>
              <button className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-900">
                <img
                  className="h-8 w-8 rounded-full"
                  src="https://avatars.githubusercontent.com/u/1?v=4"
                  alt="ユーザーアバター"
                />
                <span className="ml-2 hidden md:inline-block">Dr. 山田太郎</span>
              </button>
            </div>
          </header>
          
          <aside className="sidebar bg-white border-r border-gray-200 hidden md:block">
            <div className="p-4">
              <MainNav />
            </div>
          </aside>

          <main className="main-content bg-gray-100">
            <div className="max-w-7xl mx-auto">
              <Outlet />
            </div>
          </main>

          <MobileNav />
        </div>
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

// エラーバウンダリー
export function ErrorBoundary({ error }: { error: Error }) {
  return (
    <html lang="ja">
      <head>
        <title>エラーが発生しました</title>
        <Meta />
        <Links />
      </head>
      <body>
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
          <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
            <h1 className="text-2xl font-bold text-red-600 mb-4">
              エラーが発生しました
            </h1>
            <p className="text-gray-600 mb-4">
              申し訳ありませんが、予期せぬエラーが発生しました。
            </p>
            <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
              {error.message}
            </pre>
          </div>
        </div>
        <Scripts />
      </body>
    </html>
  );
}

