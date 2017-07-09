import React from 'react';
import styled from 'styled-components';

import AsyncComponent from './AsyncComponent';

export default class BuildJobList extends AsyncComponent {
  getEndpoints() {
    let {buildID} = this.props.params;
    return [['jobList', `/builds/${buildID}/jobs`]];
  }

  renderBody() {
    return (
      <Section>
        <List>
          {this.state.jobList.map(job => {
            return (
              <ListItem key={job.id}>
                {job.id}
              </ListItem>
            );
          })}
        </List>
      </Section>
    );
  }
}

const Section = styled.div`padding: 30px;`;

const List = styled.div`
  border: 1px solid #d8d7e0;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, .06);
`;

const ListItem = styled.div`
  border-top: 1px solid #e0e4e8;
  display: flex;
  align-items: center;
  padding: 10px 15px;

  &:first-child {
    border: 0;
  }
`;