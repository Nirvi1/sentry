import React from 'react';
import styled from '@emotion/styled';

import space from 'app/styles/space';

type Step = {
  title: React.ReactNode;
  content: React.ReactElement;
  subtitle?: string;
};

type Props = {
  steps: Array<Step>;
};

const Steps = ({steps}: Props) => (
  <Wrapper>
    {steps.map(({title, subtitle, content}, index) => (
      <Step key={index}>
        <Bullet>{index + 1}</Bullet>
        <div>
          <Title>{title}</Title>
          {subtitle && <Subtitle>{subtitle}</Subtitle>}
          {content}
        </div>
      </Step>
    ))}
  </Wrapper>
);

export default Steps;

const Wrapper = styled('div')`
  display: grid;
  grid-gap: ${space(4)};
`;

const Bullet = styled('div')`
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: ${p => p.theme.yellow400};
  font-size: ${p => p.theme.fontSizeSmall};
`;

const Title = styled('div')`
  margin-bottom: ${space(1.5)};
`;

const Subtitle = styled('div')`
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${space(1)};
`;

const Step = styled('div')`
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${space(1.5)};
`;
