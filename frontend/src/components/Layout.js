import { Outlet, useNavigate, useLocation } from 'react-router-dom';

import { TabMenu } from 'primereact/tabmenu';
import { Card } from 'primereact/card';

export function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const items = [
    {
      label: 'Spot',
      icon: 'pi pi-pencil',
      command: () => {
        navigate('/');
      },
    },
    {
      label: 'Benchmarks',
      icon: 'pi pi-list',
      command: () => {
        navigate('/benchmarks');
      },
    },
    {
      label: 'Settings',
      icon: 'pi pi-cog',
      command: () => {
        navigate('/settings');
      },
    },
  ];

  const getActiveIndex = () => {
    if (location.pathname === '/benchmarks') {
      return 1;
    } else if (location.pathname === '/settings') {
      return 2;
    } else return 0;
  };

  return (
    <Card>
      <TabMenu activeIndex={getActiveIndex()} model={items} />
      <Outlet />
    </Card>
  );
}
