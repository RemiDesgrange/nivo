<template>
  <div>
    <b-navbar type="dark" variant="dark">
      <b-navbar-brand to="/">
        Nivo
      </b-navbar-brand>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/">
            BERA
          </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav>
          <b-nav-item to="/flowcapt">
            flowcapt
          </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav>
          <b-nav-item to="/poste-nivo">
            Poste Nivo
          </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav>
          <b-nav-item to="/info">
            Infos
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
      <b-navbar-nav class="ml-auto">
        <b-nav-item href="https://github.com/RemiDesgrange/nivo">
          <b-icon-github />
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>
