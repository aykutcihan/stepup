export const translations = {
  en: {
    // Nav
    nav: {
      dashboard: 'Dashboard',
      users: 'Users',
      departments: 'Departments',
      templates: 'Templates',
      plans: 'Plans',
      auditTrail: 'Audit Trail',
      reports: 'Reports',
    },
    // Menu
    menu: {
      myProfile: 'My Profile',
      appearance: 'Appearance',
      language: 'Language',
      logout: 'Logout',
    },
    // Theme
    theme: {
      light: 'Light',
      dark: 'Dark',
      system: 'System',
    },
    // Language names
    languages: {
      en: 'English',
      nl: 'Nederlands',
    },
    // Users page
    users: {
      title: 'Users',
      subtitle: 'Manage users, roles and department assignments.',
      inviteUser: '+ Invite User',
      allRoles: 'All roles',
      allDepartments: 'All departments',
      allStatuses: 'All statuses',
      active: 'Active',
      inactive: 'Inactive',
      noUsers: 'No users found.',
      columns: {
        name: 'Name',
        email: 'Email',
        role: 'Role',
        department: 'Department',
        status: 'Status',
        actions: 'Actions',
      },
      you: '(you)',
      noDepartment: 'No department',
      actions: {
        deactivate: 'Deactivate',
        reactivate: 'Reactivate',
      },
    },
    // Departments page
    departments: {
      title: 'Departments',
      subtitle: "Manage your organisation's departments.",
      addDepartment: '+ Add Department',
      cancel: 'Cancel',
      noDepartments: 'No departments yet.',
      departmentName: 'Department name',
      add: 'Add',
      save: 'Save',
      columns: {
        name: 'Name',
        status: 'Status',
        actions: 'Actions',
      },
      actions: {
        rename: 'Rename',
        deactivate: 'Deactivate',
        reactivate: 'Reactivate',
      },
    },
    // Audit Trail
    audit: {
      title: 'Audit Trail',
      subtitle: 'System activity log for all key actions.',
      noLogs: 'No audit logs found.',
      loading: 'Loading...',
      entries: (n: number) => `${n} ${n === 1 ? 'entry' : 'entries'} found`,
      filters: {
        action: 'Action',
        entity: 'Entity',
        from: 'From',
        to: 'To',
        allActions: 'All actions',
        allEntities: 'All entities',
        clearFilters: 'Clear filters',
      },
      columns: {
        date: 'Date',
        actor: 'Actor',
        action: 'Action',
        entity: 'Entity',
        detail: 'Detail',
      },
    },
    // Common
    common: {
      active: 'Active',
      inactive: 'Inactive',
    },
  },

  nl: {
    // Nav
    nav: {
      dashboard: 'Dashboard',
      users: 'Gebruikers',
      departments: 'Afdelingen',
      templates: 'Sjablonen',
      plans: 'Plannen',
      auditTrail: 'Auditspoor',
      reports: 'Rapporten',
    },
    // Menu
    menu: {
      myProfile: 'Mijn profiel',
      appearance: 'Weergave',
      language: 'Taal',
      logout: 'Uitloggen',
    },
    // Theme
    theme: {
      light: 'Licht',
      dark: 'Donker',
      system: 'Systeem',
    },
    // Language names
    languages: {
      en: 'English',
      nl: 'Nederlands',
    },
    // Users page
    users: {
      title: 'Gebruikers',
      subtitle: 'Beheer gebruikers, rollen en afdelingstoewijzingen.',
      inviteUser: '+ Gebruiker uitnodigen',
      allRoles: 'Alle rollen',
      allDepartments: 'Alle afdelingen',
      allStatuses: 'Alle statussen',
      active: 'Actief',
      inactive: 'Inactief',
      noUsers: 'Geen gebruikers gevonden.',
      columns: {
        name: 'Naam',
        email: 'E-mail',
        role: 'Rol',
        department: 'Afdeling',
        status: 'Status',
        actions: 'Acties',
      },
      you: '(jij)',
      noDepartment: 'Geen afdeling',
      actions: {
        deactivate: 'Deactiveren',
        reactivate: 'Reactiveren',
      },
    },
    // Departments page
    departments: {
      title: 'Afdelingen',
      subtitle: 'Beheer de afdelingen van uw organisatie.',
      addDepartment: '+ Afdeling toevoegen',
      cancel: 'Annuleren',
      noDepartments: 'Nog geen afdelingen.',
      departmentName: 'Afdelingsnaam',
      add: 'Toevoegen',
      save: 'Opslaan',
      columns: {
        name: 'Naam',
        status: 'Status',
        actions: 'Acties',
      },
      actions: {
        rename: 'Hernoemen',
        deactivate: 'Deactiveren',
        reactivate: 'Reactiveren',
      },
    },
    // Audit Trail
    audit: {
      title: 'Auditspoor',
      subtitle: 'Systeemactiviteitenlogboek voor alle belangrijke acties.',
      noLogs: 'Geen auditlogboeken gevonden.',
      loading: 'Laden...',
      entries: (n: number) => `${n} ${n === 1 ? 'vermelding' : 'vermeldingen'} gevonden`,
      filters: {
        action: 'Actie',
        entity: 'Entiteit',
        from: 'Van',
        to: 'Tot',
        allActions: 'Alle acties',
        allEntities: 'Alle entiteiten',
        clearFilters: 'Filters wissen',
      },
      columns: {
        date: 'Datum',
        actor: 'Uitvoerder',
        action: 'Actie',
        entity: 'Entiteit',
        detail: 'Detail',
      },
    },
    // Common
    common: {
      active: 'Actief',
      inactive: 'Inactief',
    },
  },
} as const
