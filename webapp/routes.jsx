import React from 'react';
import {IndexRoute, Route, IndexRedirect} from 'react-router';

import App from './pages/App';
import BuildCoverage from './pages/BuildCoverage';
import BuildDetails from './pages/BuildDetails';
import BuildDiff from './pages/BuildDiff';
import BuildOverview from './pages/BuildOverview';
import BuildTestList from './pages/BuildTestList';
import GitHubRepositoryList from './pages/GitHubRepositoryList';
import OwnerDetails from './pages/OwnerDetails';
import RepositoryDetails from './pages/RepositoryDetails';
import RepositoryBuildList from './pages/RepositoryBuildList';
import RepositoryHooks from './pages/RepositoryHooks';
import RepositoryHookDetails from './pages/RepositoryHookDetails';
import RepositoryRevisionList from './pages/RepositoryRevisionList';
import RepositorySettingsLayout from './pages/RepositorySettingsLayout';
import RepositorySettings from './pages/RepositorySettings';
import RepositoryTests from './pages/RepositoryTests';
import RepositoryTestList from './pages/RepositoryTestList';
import RepositoryTestTree from './pages/RepositoryTestTree';
import UserBuildList from './pages/UserBuildList';

import Login from './components/Login';
import NotFoundError from './components/NotFoundError';

import requireAuth from './utils/requireAuth';

export default (
  <Route path="/" component={App}>
    <IndexRedirect to="/builds" />
    <Route path="/settings/github/repos" component={requireAuth(GitHubRepositoryList)} />
    <Route path="/builds" component={requireAuth(UserBuildList)} />
    <Route path="/login" component={Login} />
    <Route path="/:provider/:ownerName" component={requireAuth(OwnerDetails)} />
    <Route
      path="/:provider/:ownerName/:repoName"
      component={requireAuth(RepositoryDetails)}>
      <IndexRoute component={requireAuth(RepositoryRevisionList)} />
      <Route path="builds" component={RepositoryBuildList} />
      <Route path="settings" component={RepositorySettingsLayout}>
        <IndexRoute component={RepositorySettings} />
        <Route path="hooks" component={RepositoryHooks} />
        <Route path="hooks/:hookId" component={RepositoryHookDetails} />
      </Route>
      <Route path="tests" component={RepositoryTests}>
        <IndexRoute component={RepositoryTestTree} />
        <Route path="all" component={RepositoryTestList} />
      </Route>
      <Route path="builds/:buildNumber" component={BuildDetails}>
        <IndexRoute component={BuildOverview} />
        <Route path="coverage" component={BuildCoverage} />
        <Route path="diff" component={BuildDiff} />
        <Route path="tests" component={BuildTestList} />
      </Route>
    </Route>
    <Route path="*" component={NotFoundError} />
  </Route>
);
