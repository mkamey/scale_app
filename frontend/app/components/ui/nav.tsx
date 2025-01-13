import { Link, useLocation } from "@remix-run/react";
import {
  LayoutDashboard,
  Users,
  ClipboardList,
  FileText,
  Settings,
  type LucideIcon,
} from "lucide-react";

interface NavItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

const navItems: NavItem[] = [
  {
    label: "ダッシュボード",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    label: "患者一覧",
    href: "/patients",
    icon: Users,
  },
  {
    label: "検査一覧",
    href: "/assessments",
    icon: ClipboardList,
  },
  {
    label: "レポート",
    href: "/reports",
    icon: FileText,
  },
  {
    label: "設定",
    href: "/settings",
    icon: Settings,
  },
];

export function MainNav() {
  const location = useLocation();

  return (
    <nav className="space-y-1">
      {navItems.map((item) => {
        const isActive = location.pathname === item.href;
        const Icon = item.icon;

        return (
          <Link
            key={item.href}
            to={item.href}
            className={`
              flex items-center px-4 py-2 text-sm font-medium rounded-md
              ${
                isActive
                  ? "bg-gray-100 text-blue-600"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              }
            `}
          >
            <Icon
              className={`mr-3 h-5 w-5 ${
                isActive ? "text-blue-600" : "text-gray-400"
              }`}
            />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}

export function MobileNav() {
  const location = useLocation();

  return (
    <nav className="flex items-center justify-around fixed bottom-0 w-full bg-white border-t border-gray-200 p-2 md:hidden">
      {navItems.map((item) => {
        const isActive = location.pathname === item.href;
        const Icon = item.icon;

        return (
          <Link
            key={item.href}
            to={item.href}
            className={`
              flex flex-col items-center justify-center p-2 rounded-md
              ${isActive ? "text-blue-600" : "text-gray-600"}
            `}
          >
            <Icon className="h-5 w-5" />
            <span className="text-xs mt-1">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}